"""
Zipline Dynamic Pricing Model - V2 IMPROVED
===========================================

Key improvements:
1. Lower price elasticity (users are less price-sensitive than assumed)
2. More moderate surge pricing (don't price people out)
3. Better balance between blocking reduction and revenue maximization
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple


class ZiplineDynamicPricingV2:
    """
    IMPROVED dynamic pricing model with better calibration.
    
    Changes from V1:
    - More moderate capacity thresholds
    - Lower maximum multipliers
    - Better revenue optimization
    """
    
    def __init__(self):
        # Drone capacity by hub
        self.hub_capacity = {
            **{i: 5 for i in range(5)},
            **{i: 9 for i in range(5, 10)},
            **{i: 15 for i in range(10, 15)}
        }
        
        # Base prices - slightly higher to improve revenue
        self.base_prices = {
            'Grocery': 4.99,  # Up from 3.99
            'Meal': 5.99,     # Up from 4.99
            'Pharma': 7.99    # Up from 6.99
        }
        
        # Maximum prices - keep competitive
        self.max_prices = {
            'Grocery': 10.99,  # Down from 12.99 (too aggressive)
            'Meal': 13.99,     # Down from 15.99
            'Pharma': 17.99    # Down from 19.99
        }
        
        # IMPROVED: More conservative capacity thresholds
        self.capacity_thresholds = {
            'low': 0.4,      # 40% - start discounting earlier
            'medium': 0.6,   # 60% - normal pricing range
            'high': 0.80,    # 80% - start surging (not 70%)
            'critical': 0.90 # 90% - aggressive surge (not 85%)
        }
        
        # Flight parameters
        self.loading_time_min = 2
        self.takeoff_time_min = 1
        self.landing_time_min = 1
        self.delivery_time_min = 1
        self.cruise_speed_mph = 70
        
    def calculate_delivery_time(self, distance_miles: float) -> float:
        """Calculate total delivery time in minutes for round trip."""
        cruise_time = (distance_miles / self.cruise_speed_mph) * 60
        total_time = (
            self.loading_time_min +
            self.takeoff_time_min +
            cruise_time +
            self.landing_time_min +
            self.delivery_time_min +
            cruise_time
        )
        return total_time
    
    def get_price_multiplier(
        self,
        utilization: float,
        order_type: str,
        distance_miles: float
    ) -> float:
        """
        IMPROVED price multiplier calculation.
        
        Key changes:
        - More moderate multipliers
        - Smoother transitions
        - Better revenue optimization
        """
        # IMPROVED: More moderate base multipliers
        if utilization < self.capacity_thresholds['low']:
            # Low demand: modest discount
            base_multiplier = 0.85  # Was 0.7 - too aggressive
        elif utilization < self.capacity_thresholds['medium']:
            # Medium demand: base price
            base_multiplier = 1.0
        elif utilization < self.capacity_thresholds['high']:
            # Getting busy: modest surge
            base_multiplier = 1.15  # Was 1.3 - too aggressive
        elif utilization < self.capacity_thresholds['critical']:
            # High demand: moderate surge
            base_multiplier = 1.35  # Was 1.6 - too aggressive
        else:
            # Critical: strong surge to prevent blocking
            base_multiplier = 1.60  # Was 2.0 - too aggressive
        
        # Distance adjustment - same as before
        if distance_miles > 9:
            distance_multiplier = 1.15  # Was 1.2
        elif distance_miles > 6:
            distance_multiplier = 1.08  # Was 1.1
        else:
            distance_multiplier = 1.0
        
        # IMPROVED: Less differentiation by order type
        # Your data shows users aren't that price-sensitive
        type_sensitivity = {
            'Pharma': 1.0,   # Full multiplier
            'Meal': 0.95,    # Was 0.9 - slight reduction
            'Grocery': 0.90  # Was 0.8 - moderate reduction
        }
        
        final_multiplier = base_multiplier * distance_multiplier * type_sensitivity[order_type]
        
        return final_multiplier
    
    def calculate_price(
        self,
        nest_id: int,
        order_type: str,
        distance_miles: float,
        utilization: float
    ) -> float:
        """Calculate dynamic price."""
        base_price = self.base_prices[order_type]
        max_price = self.max_prices[order_type]
        
        multiplier = self.get_price_multiplier(utilization, order_type, distance_miles)
        price = base_price * multiplier
        price = min(price, max_price)
        
        # Round to nearest $0.99
        price = np.floor(price) + 0.99
        
        return price


# Quick test
if __name__ == "__main__":
    model = ZiplineDynamicPricingV2()
    
    print("IMPROVED MODEL - Price Examples")
    print("="*60)
    
    utilizations = [0.3, 0.5, 0.7, 0.85, 0.95]
    
    for order_type in ['Grocery', 'Meal', 'Pharma']:
        print(f"\n{order_type} (7 miles):")
        for util in utilizations:
            price = model.calculate_price(
                nest_id=5,
                order_type=order_type,
                distance_miles=7.0,
                utilization=util
            )
            print(f"  {util*100:>4.0f}% utilization → ${price:>5.2f}")
