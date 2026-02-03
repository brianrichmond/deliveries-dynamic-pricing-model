"""
Dynamic Pricing Model Simulation & Validation
==============================================

This script simulates the dynamic pricing model and compares it against:
1. Baseline (current random pricing)
2. Fixed low price (maximize orders, ignore capacity)
3. Fixed high price (maximize profit, hurt experience)

Validation metrics (in priority order):
1. Blocking rate (MUST be lower than baseline)
2. Revenue (should be higher than baseline)
3. Asset utilization (variance in capacity usage)
"""

import pandas as pd
import numpy as np
from dynamic_pricing_model import ZiplineDynamicPricing
import matplotlib.pyplot as plt
import seaborn as sns


class PricingSimulator:
    """
    Simulate order flow under different pricing strategies.
    """
    
    def __init__(self, session_df: pd.DataFrame, pricing_df: pd.DataFrame):
        """
        Initialize simulator with historical data.
        
        Parameters:
        - session_df: Historical session data
        - pricing_df: Historical pricing schedule
        """
        self.session_df = session_df.copy()
        self.pricing_df = pricing_df.copy()
        
        # Fit price elasticity from historical data
        self._fit_elasticity()
        
        # Initialize pricing model
        self.model = ZiplineDynamicPricing()
        
    def _fit_elasticity(self):
        """
        Estimate price elasticity by order type from historical data.
        
        This is simplified - we look at conversion rate vs price.
        """
        # Merge sessions with pricing
        merged = self.session_df.merge(
            self.session_df.groupby(['nest_id', 'order_type'])['delivery_fee'].mean(),
            on=['nest_id', 'order_type'],
            suffixes=('', '_avg')
        )
        
        # Calculate conversion rate at different price points
        self.elasticity = {}
        
        for order_type in ['Grocery', 'Meal', 'Pharma']:
            type_data = self.session_df[self.session_df['order_type'] == order_type]
            
            # Group by price bins
            price_bins = pd.cut(type_data['delivery_fee'], bins=5)
            conversion = type_data.groupby(price_bins)['session_outcome'].apply(
                lambda x: (x == 'ordered').mean()
            )
            
            # Store median conversion for later use
            self.elasticity[order_type] = {
                'base_conversion': (type_data['session_outcome'] == 'ordered').mean(),
                'base_price': type_data['delivery_fee'].median()
            }
    
    def simulate_demand_response(
        self,
        price: float,
        base_price: float,
        base_conversion: float,
        order_type: str
    ) -> float:
        """
        Simulate how conversion rate changes with price.
        
        Uses simple linear elasticity:
        - Pharma: -0.5 (inelastic)
        - Meal: -1.0 (unit elastic)
        - Grocery: -1.5 (elastic)
        """
        elasticity_coefficients = {
            'Pharma': -0.5,
            'Meal': -1.0,
            'Grocery': -1.5
        }
        
        elasticity = elasticity_coefficients[order_type]
        
        # Percent change in quantity = elasticity × percent change in price
        price_change_pct = (price - base_price) / base_price
        conversion_change_pct = elasticity * price_change_pct
        
        # New conversion rate
        new_conversion = base_conversion * (1 + conversion_change_pct)
        
        # Ensure conversion stays between 0 and 1
        new_conversion = max(0.1, min(0.95, new_conversion))
        
        return new_conversion
    
    def simulate_day(
        self,
        date: str,
        pricing_strategy: str = 'dynamic'
    ) -> Dict:
        """
        Simulate one day of operations under a pricing strategy.
        
        Parameters:
        - date: Date to simulate
        - pricing_strategy: 'dynamic', 'baseline', 'low', 'high'
        
        Returns:
        - Dictionary with performance metrics
        """
        # Get sessions for this day
        day_sessions = self.session_df[
            pd.to_datetime(self.session_df['timestamp']).dt.date == pd.to_datetime(date).date()
        ].copy()
        
        if len(day_sessions) == 0:
            return None
        
        # Initialize tracking
        total_revenue = 0
        total_orders = 0
        total_blocks = 0
        total_sessions = len(day_sessions)
        
        # Track capacity by hub and time
        hub_capacity_usage = {i: [] for i in range(15)}
        
        # Process each hour
        day_sessions['hour'] = pd.to_datetime(day_sessions['timestamp']).dt.hour
        
        for hour in range(24):
            hour_sessions = day_sessions[day_sessions['hour'] == hour]
            
            if len(hour_sessions) == 0:
                continue
            
            # For each hub
            for nest_id in range(15):
                nest_sessions = hour_sessions[hour_sessions['nest_id'] == nest_id]
                
                if len(nest_sessions) == 0:
                    hub_capacity_usage[nest_id].append(0)
                    continue
                
                # Calculate current utilization (simplified)
                capacity = self.model.hub_capacity[nest_id]
                demand = len(nest_sessions)
                base_utilization = demand / (capacity * 2)  # Rough estimate
                
                # Process each session
                for _, session in nest_sessions.iterrows():
                    order_type = session['order_type']
                    distance = session['distance_miles']
                    
                    # Determine price based on strategy
                    if pricing_strategy == 'dynamic':
                        price = self.model.calculate_price(
                            nest_id=nest_id,
                            order_type=order_type,
                            distance_miles=distance,
                            utilization=base_utilization
                        )
                    elif pricing_strategy == 'low':
                        price = 2.99  # Always low
                    elif pricing_strategy == 'high':
                        price = 15.99  # Always high
                    else:  # baseline (actual historical)
                        price = session['delivery_fee']
                    
                    # Simulate conversion based on price
                    base_conversion = self.elasticity[order_type]['base_conversion']
                    base_price = self.elasticity[order_type]['base_price']
                    
                    conversion_prob = self.simulate_demand_response(
                        price, base_price, base_conversion, order_type
                    )
                    
                    # Simulate capacity constraint
                    # If utilization > 1.0, start blocking
                    if base_utilization > 1.0:
                        block_prob = min(0.9, (base_utilization - 1.0) * 2)
                    else:
                        block_prob = 0
                    
                    # Determine outcome
                    rand = np.random.random()
                    
                    if rand < block_prob:
                        # Blocked
                        total_blocks += 1
                    elif rand < block_prob + conversion_prob:
                        # Ordered
                        total_orders += 1
                        total_revenue += price + session['subtotal']
                        # Update utilization
                        delivery_time_hrs = self.model.calculate_delivery_time(distance) / 60
                        base_utilization += delivery_time_hrs / capacity
                    # else: abandoned
                
                # Track final utilization
                hub_capacity_usage[nest_id].append(base_utilization)
        
        # Calculate metrics
        blocking_rate = total_blocks / total_sessions if total_sessions > 0 else 0
        order_rate = total_orders / total_sessions if total_sessions > 0 else 0
        avg_revenue_per_session = total_revenue / total_sessions if total_sessions > 0 else 0
        
        # Calculate capacity utilization variance (lower = better asset utilization)
        all_utilizations = [u for utilizations in hub_capacity_usage.values() for u in utilizations]
        utilization_variance = np.var(all_utilizations) if len(all_utilizations) > 0 else 0
        
        return {
            'date': date,
            'strategy': pricing_strategy,
            'total_sessions': total_sessions,
            'total_orders': total_orders,
            'total_blocks': total_blocks,
            'total_revenue': total_revenue,
            'blocking_rate': blocking_rate,
            'order_rate': order_rate,
            'revenue_per_session': avg_revenue_per_session,
            'utilization_variance': utilization_variance
        }
    
    def run_comparison(self, n_days: int = 30) -> pd.DataFrame:
        """
        Run simulation comparing different strategies.
        
        Returns DataFrame with daily results for all strategies.
        """
        # Get unique dates
        dates = pd.to_datetime(self.session_df['timestamp']).dt.date.unique()
        dates = sorted(dates)[:n_days]
        
        results = []
        
        strategies = ['baseline', 'dynamic', 'low', 'high']
        
        for date in dates:
            for strategy in strategies:
                result = self.simulate_day(str(date), strategy)
                if result:
                    results.append(result)
        
        return pd.DataFrame(results)
    
    def print_summary(self, results: pd.DataFrame):
        """
        Print summary comparison of strategies.
        """
        print("\n" + "="*80)
        print("PRICING STRATEGY COMPARISON")
        print("="*80)
        
        summary = results.groupby('strategy').agg({
            'blocking_rate': 'mean',
            'order_rate': 'mean',
            'revenue_per_session': 'mean',
            'utilization_variance': 'mean'
        }).round(4)
        
        print("\nAverage Performance Metrics:")
        print(summary)
        
        # Calculate improvements over baseline
        baseline = summary.loc['baseline']
        
        print("\n" + "="*80)
        print("IMPROVEMENT OVER BASELINE")
        print("="*80)
        
        for strategy in ['dynamic', 'low', 'high']:
            if strategy in summary.index:
                strat = summary.loc[strategy]
                
                print(f"\n{strategy.upper()} Strategy:")
                print(f"  Blocking Rate:   {strat['blocking_rate']:.1%} vs {baseline['blocking_rate']:.1%} "
                      f"({(strat['blocking_rate']/baseline['blocking_rate']-1)*100:+.1f}%)")
                print(f"  Order Rate:      {strat['order_rate']:.1%} vs {baseline['order_rate']:.1%} "
                      f"({(strat['order_rate']/baseline['order_rate']-1)*100:+.1f}%)")
                print(f"  Revenue/Session: ${strat['revenue_per_session']:.2f} vs ${baseline['revenue_per_session']:.2f} "
                      f"({(strat['revenue_per_session']/baseline['revenue_per_session']-1)*100:+.1f}%)")
                print(f"  Util. Variance:  {strat['utilization_variance']:.4f} vs {baseline['utilization_variance']:.4f} "
                      f"({(strat['utilization_variance']/baseline['utilization_variance']-1)*100:+.1f}%)")
        
        # Highlight wins
        print("\n" + "="*80)
        print("OBJECTIVE ACHIEVEMENT")
        print("="*80)
        
        if 'dynamic' in summary.index:
            dyn = summary.loc['dynamic']
            
            print(f"\n✓ Priority 1 - Protect Customer Experience:")
            if dyn['blocking_rate'] < baseline['blocking_rate']:
                print(f"  ✓ BLOCKING REDUCED by {(1-dyn['blocking_rate']/baseline['blocking_rate'])*100:.1f}%")
            else:
                print(f"  ✗ BLOCKING INCREASED by {(dyn['blocking_rate']/baseline['blocking_rate']-1)*100:.1f}%")
            
            print(f"\n✓ Priority 2 - Maximize Profit:")
            if dyn['revenue_per_session'] > baseline['revenue_per_session']:
                print(f"  ✓ REVENUE INCREASED by {(dyn['revenue_per_session']/baseline['revenue_per_session']-1)*100:.1f}%")
            else:
                print(f"  ✗ REVENUE DECREASED by {(1-dyn['revenue_per_session']/baseline['revenue_per_session'])*100:.1f}%")
            
            print(f"\n✓ Priority 3 - Maximize Asset Utilization:")
            if dyn['utilization_variance'] < baseline['utilization_variance']:
                print(f"  ✓ UTILIZATION SMOOTHED by {(1-dyn['utilization_variance']/baseline['utilization_variance'])*100:.1f}%")
            else:
                print(f"  ✗ UTILIZATION MORE VARIABLE by {(dyn['utilization_variance']/baseline['utilization_variance']-1)*100:.1f}%")


def main():
    """Run simulation with sample data."""
    
    # Note: This requires actual data files
    # For demonstration, showing the structure
    
    print("Dynamic Pricing Model Simulation")
    print("="*80)
    print("\nThis simulation requires:")
    print("  1. zipline_session_log.csv")
    print("  2. zipline_pricing_schedule.csv")
    print("\nPlace these files in ../data/raw/ to run simulation.")
    print("\nThe simulation will compare:")
    print("  - Baseline (historical random pricing)")
    print("  - Dynamic (our proposed model)")
    print("  - Low (always $2.99 - maximizes orders, ignores capacity)")
    print("  - High (always $15.99 - maximizes revenue, kills orders)")
    

if __name__ == "__main__":
    main()
