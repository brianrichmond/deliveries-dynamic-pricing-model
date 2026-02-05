"""
Zipline Dynamic Pricing Model - FINAL CALIBRATED VERSION
=========================================================

Calibrated with actual data showing:
- Pharma: ~85% conversion (flat) → Nearly inelastic
- Meal: 55% → 49% conversion → Modest elasticity
- Grocery: 43% → 35% conversion → Moderate elasticity
- Higher prices REDUCE blocking (5.3% → 3.3% for Meal)
- Higher prices INCREASE revenue per session

This is the IDEAL scenario for dynamic pricing!
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple


class ZiplineDynamicPricingFinal:
    """
    Final calibrated dynamic pricing model based on real data analysis.
    """
    
    def __init__(self):
        # Drone capacity by hub
        self.hub_capacity = {
            **{i: 5 for i in range(5)},
            **{i: 9 for i in range(5, 10)},
            **{i: 15 for i in range(10, 15)}
        }
        
        # UPDATED: Base prices based on revenue-optimal analysis
        self.base_prices = {
            'Grocery': 5.49,  # Up from 4.99 (data shows $4.5+ is optimal)
            'Meal': 5.99,     # Optimal range
            'Pharma': 8.99    # Up from 7.99 (inelastic, can charge premium)
        }
        
        # Maximum prices - competitive with market surge
        self.max_prices = {
            'Grocery': 12.99,
            'Meal': 15.99,
            'Pharma': 19.99
        }
        
        # Capacity thresholds - start surging at 75% to prevent blocking
        self.capacity_thresholds = {
            'low': 0.40,     # <40% - discount to attract demand
            'medium': 0.60,  # 40-60% - base price
            'high': 0.75,    # 60-75% - start moderate surge
            'critical': 0.90 # >75% - aggressive surge to prevent blocking
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
        Calculate price multiplier based on capacity, order type, and distance.
        
        Calibrated to balance blocking reduction and revenue maximization.
        """
        # Base multiplier from capacity utilization
        if utilization < self.capacity_thresholds['low']:
            # Low demand: modest discount to fill capacity
            base_multiplier = 0.80  # 20% discount
        elif utilization < self.capacity_thresholds['medium']:
            # Medium demand: base price
            base_multiplier = 1.0
        elif utilization < self.capacity_thresholds['high']:
            # Getting busy: start moderate surge
            base_multiplier = 1.20  # 20% surge
        elif utilization < self.capacity_thresholds['critical']:
            # High demand: strong surge
            base_multiplier = 1.45  # 45% surge
        else:
            # Critical: maximum surge to prevent blocking
            base_multiplier = 1.75  # 75% surge
        
        # Distance adjustment
        if distance_miles > 9:
            distance_multiplier = 1.15  # Long trips tie up capacity
        elif distance_miles > 6:
            distance_multiplier = 1.08
        else:
            distance_multiplier = 1.0
        
        # Order type sensitivity (based on actual elasticity)
        type_sensitivity = {
            'Pharma': 1.05,  # Can charge MORE (inelastic)
            'Meal': 1.0,     # Standard multiplier
            'Grocery': 0.95  # Slight reduction (most sensitive)
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
        """Calculate dynamic price for an order."""
        base_price = self.base_prices[order_type]
        max_price = self.max_prices[order_type]
        
        multiplier = self.get_price_multiplier(utilization, order_type, distance_miles)
        price = base_price * multiplier
        price = min(price, max_price)
        
        # Round to nearest $0.99
        price = np.floor(price) + 0.99
        
        return price


if __name__ == "__main__":
    model = ZiplineDynamicPricingFinal()
    
    print("FINAL CALIBRATED MODEL - Price Examples")
    print("="*70)
    print("\nBased on real data analysis showing:")
    print("  - Pharma: 84-86% conversion (flat) → Inelastic")
    print("  - Meal: 55% → 49% conversion → Modest elasticity")
    print("  - Grocery: 43% → 35% conversion → Moderate elasticity")
    print("  - Higher prices reduce blocking AND increase revenue!")
    print("\n" + "="*70)
    
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
            
            if util < 0.4:
                status = "DISCOUNT (attract demand)"
            elif util < 0.6:
                status = "BASE PRICE"
            elif util < 0.75:
                status = "MODERATE SURGE"
            elif util < 0.90:
                status = "STRONG SURGE"
            else:
                status = "MAX SURGE (prevent blocking)"
            
            print(f"  {util*100:>4.0f}% capacity → ${price:>5.2f}  ({status})")
