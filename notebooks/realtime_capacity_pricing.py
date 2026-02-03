"""
Zipline Real-Time Capacity-Based Pricing Model with Customer Tier Protection
============================================================================

SIMPLIFIED APPROACH WITH TIER PROTECTION:
- Price based on current capacity utilization
- Protect first-timers (max 10% surge) - drives 95% loyalty
- Protect loyal users (max 30% surge) - retain best customers
- Full surge for occasional/unknown users - throttle demand intelligently
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple


class RealtimeCapacityPricing:
    """
    Pure real-time pricing based on actual capacity utilization.
    NOW WITH: Customer tier protection for first-timers and loyal users.
    """
    
    def __init__(self):
        # Drone capacity by hub
        self.hub_capacity = {
            **{i: 5 for i in range(5)},
            **{i: 9 for i in range(5, 10)},
            **{i: 15 for i in range(10, 15)}
        }
        
        # Base prices (slightly lower for better order rate)
        self.base_prices = {
            'Grocery': 4.99,
            'Meal': 5.49,
            'Pharma': 7.99
        }
        
        # Max prices (competitive with market)
        self.max_prices = {
            'Grocery': 11.99,
            'Meal': 14.99,
            'Pharma': 18.99
        }
        
        # THE ENTIRE PRICING STRATEGY: These 6 thresholds
        self.pricing_tiers = [
            (0.00, 0.40, 0.80),  # <40% util → 20% discount
            (0.40, 0.55, 0.95),  # 40-55% → 5% discount
            (0.55, 0.70, 1.00),  # 55-70% → base price
            (0.70, 0.82, 1.15),  # 70-82% → 15% surge
            (0.82, 0.92, 1.35),  # 82-92% → 35% surge
            (0.92, 1.00, 1.60),  # >92% → 60% surge (prevent blocking)
        ]
        
        # NEW: Customer tier protection
        self.protect_first_timers = True
        self.protect_loyal_users = True
        
        # Flight parameters
        self.loading_time_min = 2
        self.takeoff_time_min = 1
        self.landing_time_min = 1
        self.delivery_time_min = 1
        self.cruise_speed_mph = 70
        
    def calculate_delivery_time(self, distance_miles: float) -> float:
        """Calculate round-trip delivery time in minutes."""
        cruise_time = (distance_miles / self.cruise_speed_mph) * 60
        return (
            self.loading_time_min +
            self.takeoff_time_min +
            cruise_time +
            self.landing_time_min +
            self.delivery_time_min +
            cruise_time
        )
    
    def get_price_multiplier(
        self,
        utilization: float,
        order_type: str,
        distance_miles: float,
        user_session_count: int = None
    ) -> float:
        """
        THE CORE PRICING LOGIC with customer tier protection.
        
        NEW: Protects first-timers and loyal customers from aggressive surge.
        """
        # Find the right tier based on utilization
        base_multiplier = 1.0
        for min_util, max_util, multiplier in self.pricing_tiers:
            if min_util <= utilization < max_util:
                base_multiplier = multiplier
                break
        
        # If over 100% capacity, maximum surge
        if utilization >= 1.0:
            base_multiplier = 1.60
        
        # NEW: Customer tier protection
        if user_session_count is not None:
            if user_session_count == 0 and self.protect_first_timers:
                # First-timers: cap at 10% surge (protect first impression!)
                base_multiplier = min(base_multiplier, 1.10)
            elif user_session_count >= 3 and self.protect_loyal_users:
                # Loyal users (3+ orders): cap at 30% surge (protect best customers!)
                base_multiplier = min(base_multiplier, 1.30)
            # Else: occasional users get full surge (no cap)
        
        # Distance adjustment (long trips tie up capacity longer)
        if distance_miles > 9:
            distance_mult = 1.15
        elif distance_miles > 7:
            distance_mult = 1.08
        else:
            distance_mult = 1.0
        
        # Order type adjustment (minimal - based on elasticity)
        type_mult = {
            'Pharma': 1.02,   # Slightly higher (inelastic)
            'Meal': 1.0,      # Standard
            'Grocery': 0.98   # Slightly lower (elastic)
        }
        
        return base_multiplier * distance_mult * type_mult[order_type]
    
    def calculate_price(
        self,
        nest_id: int,
        order_type: str,
        distance_miles: float,
        utilization: float,
        user_session_count: int = None
    ) -> float:
        """
        Calculate price based on real-time capacity with customer tier protection.
        
        Parameters:
        - nest_id: Hub ID
        - order_type: 'Grocery', 'Meal', or 'Pharma'
        - distance_miles: Delivery distance
        - utilization: CURRENT capacity utilization (0.0 to 1.0+)
        - user_session_count: Number of previous sessions (0 = first-timer, 3+ = loyal)
        
        Returns:
        - Price to show customer (locked in once shown)
        """
        base_price = self.base_prices[order_type]
        max_price = self.max_prices[order_type]
        
        multiplier = self.get_price_multiplier(
            utilization, order_type, distance_miles, user_session_count
        )
        price = base_price * multiplier
        price = min(price, max_price)
        
        # Round to $X.99
        price = np.floor(price) + 0.99
        
        return price
    
    def explain_price(
        self,
        nest_id: int,
        order_type: str,
        distance_miles: float,
        utilization: float,
        user_session_count: int = None
    ) -> str:
        """
        Human-readable explanation of price.
        
        Useful for customer communication and debugging.
        """
        price = self.calculate_price(
            nest_id, order_type, distance_miles, utilization, user_session_count
        )
        
        # Base reason from capacity
        if utilization < 0.40:
            reason = "Low demand right now"
        elif utilization < 0.70:
            reason = "Normal pricing"
        elif utilization < 0.82:
            reason = "Busy right now"
        elif utilization < 0.92:
            reason = "High demand - limited availability"
        else:
            reason = "Very high demand - order soon for fastest delivery"
        
        # Add tier protection info
        if user_session_count is not None:
            if user_session_count == 0:
                reason += " (Welcome discount applied!)"
            elif user_session_count >= 3:
                reason += " (Loyal customer pricing)"
        
        return f"${price:.2f} - {reason} ({utilization*100:.0f}% capacity)"


# Quick demonstration
if __name__ == "__main__":
    model = RealtimeCapacityPricing()
    
    print("REAL-TIME CAPACITY-BASED PRICING WITH TIER PROTECTION")
    print("="*70)
    print("\nCustomer Tiers:")
    print("  First-Timer (session 0):  Max 10% surge - protect first impression")
    print("  Loyal (3+ sessions):      Max 30% surge - protect best customers")
    print("  Occasional (1-2 sessions): Full surge - standard pricing")
    print("  Unknown (no data):        Full surge - throttle demand")
    print("\n" + "="*70)
    
    print("\nExample: Meal Order at 90% Capacity (7 miles)")
    print("="*70)
    
    for session_count, tier_name in [(0, "First-Timer"), (1, "Occasional"), (5, "Loyal"), (None, "Unknown")]:
        price = model.calculate_price(5, 'Meal', 7.0, 0.90, session_count)
        explanation = model.explain_price(5, 'Meal', 7.0, 0.90, session_count)
        print(f"{tier_name:12s} (n={session_count}): {explanation}")
    
    print("\n" + "="*70)
    print("Pricing Across Capacity Levels (Loyal User, Meal, 7mi)")
    print("="*70)
    
    utilizations = [0.25, 0.50, 0.65, 0.75, 0.85, 0.95]
    
    for util in utilizations:
        price_new = model.calculate_price(5, 'Meal', 7.0, util, user_session_count=5)
        price_unknown = model.calculate_price(5, 'Meal', 7.0, util, user_session_count=None)
        
        print(f"{util*100:>3.0f}% → Loyal: ${price_new:>5.2f}  |  Unknown: ${price_unknown:>5.2f}")