"""
Zipline Dynamic Pricing Model
==============================

Simple, interpretable pricing algorithm that prioritizes:
1. Minimize blocking (protect customer experience)
2. Maximize profit
3. Maximize asset utilization

Key Design Principles:
- Rule-based and transparent (not a black-box ML model)
- Uses real-time capacity and demand signals
- Different pricing by order type (Pharma > Meal > Grocery elasticity)
- Distance-based adjustments (long distance = lower capacity)
- Easy to tune and explain to executives
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple


class ZiplineDynamicPricing:
    """
    Simple dynamic pricing model based on capacity utilization.
    
    Core Logic:
    - Calculate current capacity utilization (% of drones busy)
    - When utilization is high → increase price to throttle demand
    - When utilization is low → decrease price to attract demand
    - Different price sensitivity by order type
    """
    
    def __init__(self):
        # Drone capacity by hub
        self.hub_capacity = {
            **{i: 5 for i in range(5)},    # Hubs 0-4: 5 drones
            **{i: 9 for i in range(5, 10)}, # Hubs 5-9: 9 drones
            **{i: 15 for i in range(10, 15)} # Hubs 10-14: 15 drones
        }
        
        # Base prices by order type (competitive with market during low demand)
        self.base_prices = {
            'Grocery': 4.99,  # Was 3.99
            'Meal': 5.99,     # Was 4.99
            'Pharma': 7.99    # Was 6.99
        }
        
        # Maximum prices (competitive with surge pricing)
        self.max_prices = {
            'Grocery': 12.99,  # Can't go too high or we lose orders
            'Meal': 15.99,     # Moderate ceiling
            'Pharma': 19.99    # Can charge premium for urgency
        }
        
        # Capacity thresholds for pricing tiers
        self.capacity_thresholds = {
            'low': 0.4,      # Was 0.5
            'medium': 0.6,   # Was 0.7
            'high': 0.80,    # Was 0.70
            'critical': 0.90 # Was 0.95
        }
        
        # Flight time parameters (from problem statement)
        self.loading_time_min = 2
        self.takeoff_time_min = 1
        self.landing_time_min = 1
        self.delivery_time_min = 1
        self.cruise_speed_mph = 70
        
    def calculate_delivery_time(self, distance_miles: float) -> float:
        """
        Calculate total delivery time in minutes for a round trip.
        
        Round trip includes:
        - Loading: 2 min
        - Takeoff: 1 min
        - Cruise to destination: distance/70 * 60
        - Landing: 1 min
        - Delivery: 1 min
        - Return flight: distance/70 * 60
        """
        cruise_time = (distance_miles / self.cruise_speed_mph) * 60
        total_time = (
            self.loading_time_min +
            self.takeoff_time_min +
            cruise_time +  # To destination
            self.landing_time_min +
            self.delivery_time_min +
            cruise_time    # Return
        )
        return total_time
    
    def calculate_capacity_utilization(
        self, 
        active_deliveries: pd.DataFrame,
        nest_id: int,
        current_time: pd.Timestamp
    ) -> float:
        """
        Calculate current capacity utilization for a hub.
        
        Parameters:
        - active_deliveries: DataFrame of ongoing deliveries with 'completion_time'
        - nest_id: Hub ID
        - current_time: Current timestamp
        
        Returns:
        - Utilization ratio (0.0 to 1.0+)
        """
        # Count how many drones are currently busy
        active_count = len(active_deliveries[
            (active_deliveries['nest_id'] == nest_id) &
            (active_deliveries['completion_time'] > current_time)
        ])
        
        # Get total capacity for this hub
        total_capacity = self.hub_capacity[nest_id]
        
        # Calculate utilization
        utilization = active_count / total_capacity
        
        return utilization
    
    def get_price_multiplier(
        self,
        utilization: float,
        order_type: str,
        distance_miles: float
    ) -> float:
        """
        Calculate price multiplier based on capacity, order type, and distance.
        
        Logic:
        - Low utilization (<50%): Discount to attract demand
        - Medium utilization (50-70%): Base price
        - High utilization (70-85%): Moderate surge
        - Critical utilization (>85%): Aggressive surge to prevent blocking
        
        Distance adjustment:
        - Long distances reduce capacity → add premium
        """
        # Base multiplier from capacity utilization
        if utilization < self.capacity_thresholds['low']:
            base_multiplier = 0.85  # Was 0.7
        elif utilization < self.capacity_thresholds['medium']:
            base_multiplier = 1.0
        elif utilization < self.capacity_thresholds['high']:
            base_multiplier = 1.15  # Was 1.3
        elif utilization < self.capacity_thresholds['critical']:
            base_multiplier = 1.35  # Was 1.6
        else:
            base_multiplier = 1.60  # Was 2.0
        
        # Distance adjustment (long trips reduce effective capacity)
        if distance_miles > 9:
            distance_multiplier = 1.2  # 20% premium for long trips
        elif distance_miles > 6:
            distance_multiplier = 1.1  # 10% premium for medium trips
        else:
            distance_multiplier = 1.0  # No adjustment for short trips
        
        # Order type sensitivity adjustment
        # Pharma can handle higher multipliers (inelastic)
        # Grocery needs lower multipliers (elastic)
        type_sensitivity = {
            'Pharma': 1.0,   # Full multiplier (inelastic demand)
            'Meal': 0.9,     # Slightly reduced (moderate sensitivity)
            'Grocery': 0.8   # Most reduced (high sensitivity)
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
        """
        Calculate dynamic price for an order.
        
        Parameters:
        - nest_id: Hub ID
        - order_type: 'Grocery', 'Meal', or 'Pharma'
        - distance_miles: Distance to delivery location
        - utilization: Current capacity utilization (0-1+)
        
        Returns:
        - Recommended delivery fee
        """
        # Get base price and max price
        base_price = self.base_prices[order_type]
        max_price = self.max_prices[order_type]
        
        # Calculate multiplier
        multiplier = self.get_price_multiplier(utilization, order_type, distance_miles)
        
        # Apply multiplier
        price = base_price * multiplier
        
        # Cap at maximum
        price = min(price, max_price)
        
        # Round to nearest $0.99
        price = np.floor(price) + 0.99
        
        return price
    
    def get_pricing_schedule(
        self,
        demand_forecast: pd.DataFrame,
        nest_id: int,
        date: str
    ) -> pd.DataFrame:
        """
        Generate pricing schedule for a full day at a specific hub.
        
        Parameters:
        - demand_forecast: DataFrame with columns ['timestamp', 'nest_id', 'order_type', 
                          'distance_miles', 'expected_orders']
        - nest_id: Hub to generate schedule for
        - date: Date string (e.g., '2024-01-01')
        
        Returns:
        - DataFrame with pricing schedule by hour and order type
        """
        schedule = []
        
        for _, row in demand_forecast.iterrows():
            if row['nest_id'] != nest_id:
                continue
            
            # Estimate utilization from expected orders
            capacity = self.hub_capacity[nest_id]
            avg_delivery_time = self.calculate_delivery_time(row['distance_miles'])
            
            # Rough utilization: (orders/hour × avg_delivery_time_hours) / capacity
            utilization = (row['expected_orders'] * (avg_delivery_time / 60)) / capacity
            
            # Calculate price
            price = self.calculate_price(
                nest_id=nest_id,
                order_type=row['order_type'],
                distance_miles=row['distance_miles'],
                utilization=utilization
            )
            
            schedule.append({
                'timestamp': row['timestamp'],
                'nest_id': nest_id,
                'order_type': row['order_type'],
                'delivery_fee': price,
                'utilization': utilization
            })
        
        return pd.DataFrame(schedule)


# Simplified usage example
def main():
    """Example of how to use the pricing model."""
    
    # Initialize model
    model = ZiplineDynamicPricing()
    
    # Example: Calculate price for a single order
    price = model.calculate_price(
        nest_id=3,
        order_type='Meal',
        distance_miles=7.5,
        utilization=0.75  # 75% capacity utilized
    )
    
    print(f"Dynamic price for Meal order: ${price:.2f}")
    
    # Example utilization levels
    utilizations = [0.3, 0.5, 0.7, 0.85, 0.95]
    
    print("\n" + "="*60)
    print("Price Response to Capacity Utilization")
    print("="*60)
    
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


if __name__ == "__main__":
    main()
