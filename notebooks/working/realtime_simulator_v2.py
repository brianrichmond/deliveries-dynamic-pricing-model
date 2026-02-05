"""
Real-Time Capacity-Based Pricing Simulator V2
==============================================

UPDATED: Tracks BOTH delivery_fee_revenue AND total_order_value
"""

import pandas as pd
import numpy as np
from realtime_capacity_pricing import RealtimeCapacityPricing


class RealtimeSimulatorV2:
    """
    Simulates real-time capacity-based pricing.
    
    V2: Tracks both delivery fee revenue (for optimization) and total order value (for business metrics)
    """
    
    def __init__(self, session_df, model):
        self.session_df = session_df.copy()
        self.model = model
        self.base_stats = self._calculate_base_stats()
        
    def _calculate_base_stats(self):
        stats = {}
        for order_type in ['Grocery', 'Meal', 'Pharma']:
            type_data = self.session_df[self.session_df['order_type'] == order_type]
            stats[order_type] = {
                'base_conversion': (type_data['session_outcome'] == 'ordered').mean(),
                'base_price': type_data['delivery_fee'].median()
            }
        return stats
    
    def estimate_conversion(self, price, order_type, base_price):
        """Calibrated elasticity from real data."""
        elasticity = {'Pharma': -0.05, 'Meal': -0.20, 'Grocery': -0.30}
        base_conversion = self.base_stats[order_type]['base_conversion']
        
        if base_price > 0:
            price_change_pct = (price - base_price) / base_price
            conversion_change_pct = elasticity[order_type] * price_change_pct
            new_conversion = base_conversion * (1 + conversion_change_pct)
        else:
            new_conversion = base_conversion
        
        return max(0.25, min(0.95, new_conversion))
    
    def calculate_blocking_prob(self, utilization, price_effect):
        """Blocking based on actual capacity state."""
        if utilization < 0.7:
            base_block = 0.01
        elif utilization < 0.85:
            base_block = 0.05
        elif utilization < 1.0:
            base_block = 0.15
        elif utilization < 1.2:
            base_block = 0.30
        else:
            base_block = 0.50
        
        return base_block * price_effect
    
    def simulate_session(self, session, strategy, current_utilization):
        """
        Simulate ONE session with real-time pricing.
        
        V2: Returns BOTH delivery_fee_revenue and total_order_value
        """
        nest_id = int(session['nest_id'])
        order_type = session['order_type']
        distance = float(session['distance_miles'])
        subtotal = float(session['subtotal'])
        
        # Get CURRENT utilization at this hub
        util = current_utilization.get(nest_id, 0.5)
        
        # Determine price based on CURRENT capacity
        if strategy == 'baseline':
            # Use original delivery fee if available, otherwise use base_price from model
            if pd.notna(session['delivery_fee']):
                price = float(session['delivery_fee'])
            else:
                # For originally-abandoned sessions, use the base price (no surge/discount)
                price = self.model.base_prices[order_type]
        elif strategy == 'realtime':
            # Calculate user's session count for tier protection
            user_id = session.get('user_id', None)
            if user_id is not None and pd.notna(user_id):
                user_history = self.session_df[
                    (self.session_df['user_id'] == user_id) &
                    (self.session_df['timestamp'] < session['timestamp'])
                ]
                user_session_count = len(user_history)
            else:
                user_session_count = None
            
            price = self.model.calculate_price(
                nest_id=nest_id,
                order_type=order_type,
                distance_miles=distance,
                utilization=util,
                user_session_count=user_session_count
            )
        elif strategy == 'low':
            price = 2.99
        elif strategy == 'high':
            price = 12.99
        else:
            price = float(session['delivery_fee'])
        
        # Conversion probability
        base_price = self.base_stats[order_type]['base_price']
        conversion_prob = self.estimate_conversion(price, order_type, base_price)
        
        # Price effect on blocking
        price_ratio = price / base_price if base_price > 0 else 1.0
        if price_ratio > 1.5:
            price_effect = 0.70
        elif price_ratio > 1.2:
            price_effect = 0.85
        elif price_ratio < 0.8:
            price_effect = 1.2
        else:
            price_effect = 1.0
        
        # Blocking probability
        block_prob = self.calculate_blocking_prob(util, price_effect)
        
        # Simulate outcome
        rand = np.random.random()
        
        if rand < block_prob:
            outcome = 'blocked'
            delivery_fee_revenue = 0.0
            total_order_value = 0.0
        elif rand < block_prob + conversion_prob:
            outcome = 'ordered'
            
            # V2: Track BOTH metrics
            delivery_fee_revenue = float(price) if pd.notna(price) else 0.0
            total_order_value = delivery_fee_revenue + float(subtotal) if pd.notna(subtotal) else delivery_fee_revenue
            
            # Update utilization: drone is now busy
            delivery_time_hrs = self.model.calculate_delivery_time(distance) / 60
            capacity = self.model.hub_capacity[nest_id]
            current_utilization[nest_id] = min(2.0, util + (delivery_time_hrs / capacity))
        else:
            outcome = 'abandoned'
            delivery_fee_revenue = 0.0
            total_order_value = 0.0
        
        return {
            'outcome': outcome,
            'delivery_fee_revenue': delivery_fee_revenue,
            'total_order_value': total_order_value,
            'price': float(price),
            'utilization': util
        }
    
    def simulate_day(self, date, strategy):
        """
        Simulate one day, processing sessions chronologically.
        
        V2: Returns metrics for BOTH delivery fees and total order value
        """
        day_sessions = self.session_df[
            self.session_df['timestamp'].dt.date == pd.to_datetime(date).date()
        ].copy()
        
        if len(day_sessions) == 0:
            return None
        
        # Sort by timestamp (process in order)
        day_sessions = day_sessions.sort_values('timestamp')
        
        # Track utilization at each hub
        current_utilization = {i: 0.3 for i in range(15)}
        all_results = []
        
        last_hour = 0
        
        # Process each session in chronological order
        for _, session in day_sessions.iterrows():
            hour = session['timestamp'].hour
            
            # Decay utilization hourly (drones return)
            if hour != last_hour:
                for nest_id in current_utilization:
                    current_utilization[nest_id] *= 0.7
                last_hour = hour
            
            result = self.simulate_session(session, strategy, current_utilization)
            all_results.append(result)
        
        # Calculate metrics
        total_sessions = len(all_results)
        total_blocks = sum(1 for r in all_results if r['outcome'] == 'blocked')
        total_orders = sum(1 for r in all_results if r['outcome'] == 'ordered')
        
        # V2: Track BOTH delivery fee revenue and total order value
        total_delivery_fee_revenue = sum(r['delivery_fee_revenue'] for r in all_results)
        total_order_value = sum(r['total_order_value'] for r in all_results)
        
        return {
            'date': str(date),
            'strategy': strategy,
            'sessions': total_sessions,
            'blocks': total_blocks,
            'orders': total_orders,
            
            # V2: Delivery fee metrics (what we're optimizing)
            'delivery_fee_revenue': float(total_delivery_fee_revenue),
            'delivery_fee_per_order': float(total_delivery_fee_revenue / total_orders) if total_orders > 0 else 0.0,
            'delivery_fee_per_session': float(total_delivery_fee_revenue / total_sessions) if total_sessions > 0 else 0.0,
            
            # V2: Total order value metrics (for business context)
            'total_order_value': float(total_order_value),
            'total_value_per_order': float(total_order_value / total_orders) if total_orders > 0 else 0.0,
            'total_value_per_session': float(total_order_value / total_sessions) if total_sessions > 0 else 0.0,
            
            # Standard metrics
            'blocking_rate': total_blocks / total_sessions if total_sessions > 0 else 0,
            'order_rate': total_orders / total_sessions if total_sessions > 0 else 0,
        }
    
    def run_comparison(self, n_days=None):
        dates = sorted(self.session_df['timestamp'].dt.date.unique())
        if n_days:
            dates = dates[:n_days]
        
        strategies = ['baseline', 'realtime', 'low', 'high']
        results = []
        
        print(f"Running V2 simulation on {len(dates)} days...")
        print("Tracking: delivery_fee_revenue AND total_order_value")
        
        for i, date in enumerate(dates):
            for strategy in strategies:
                result = self.simulate_day(str(date), strategy)
                if result:
                    results.append(result)
            
            if (i + 1) % 5 == 0:
                print(f"  {i+1}/{len(dates)} complete")
        
        print("✓ Simulation complete!")
        return pd.DataFrame(results)


# Quick demo
if __name__ == "__main__":
    print("REAL-TIME SIMULATOR V2")
    print("=" * 70)
    print("\nNew in V2:")
    print("✓ Tracks delivery_fee_revenue (for pricing optimization)")
    print("✓ Tracks total_order_value (for business metrics)")
    print("✓ Provides both per-order and per-session metrics")
    print("\nMetrics available:")
    print("  - delivery_fee_revenue, delivery_fee_per_order, delivery_fee_per_session")
    print("  - total_order_value, total_value_per_order, total_value_per_session")
    print("  - blocking_rate, order_rate")
