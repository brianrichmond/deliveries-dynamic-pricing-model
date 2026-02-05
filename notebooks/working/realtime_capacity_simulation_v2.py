#!/usr/bin/env python3
"""
Real-Time Capacity Simulation V2 - Python Script Version
=========================================================

This is a Python script version that can be converted to Jupyter notebook.
Run this to generate all the analysis and plots.

Key Updates in V2:
- Tracks BOTH delivery_fee_revenue and total_order_value
- Generates separate plots for each metric
- Fixes the revenue calculation bug from V1
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from datetime import datetime

warnings.filterwarnings('ignore')
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (14, 6)
np.random.seed(42)

print("="*80)
print("REAL-TIME CAPACITY-BASED PRICING SIMULATION V2")
print("="*80)
print("\nV2 Updates:")
print("✓ Tracks delivery_fee_revenue (pricing optimization)")
print("✓ Tracks total_order_value (business metrics)")
print("✓ Dual plotting for both metrics")
print("="*80)

# Import the V2 simulator
from realtime_simulator_v2 import RealtimeSimulatorV2
from realtime_capacity_pricing import RealtimeCapacityPricing

# Load data
print("\n📊 Loading data...")
SESSION_FILE = '/mnt/user-data/uploads/zipline_session_log__5_.csv'

session_df = pd.read_csv(SESSION_FILE)
session_df['timestamp'] = pd.to_datetime(session_df['timestamp'])
session_df['delivery_fee'] = pd.to_numeric(session_df['delivery_fee'], errors='coerce')
session_df['subtotal'] = pd.to_numeric(session_df['subtotal'], errors='coerce')
session_df['distance_miles'] = pd.to_numeric(session_df['distance_miles'], errors='coerce')
session_df['subtotal'] = session_df['subtotal'].fillna(session_df['subtotal'].median())

print(f"✓ Loaded {len(session_df):,} sessions")

# Initialize model
print("\n🤖 Loading pricing model...")
model = RealtimeCapacityPricing()
print("✓ Model loaded")

# Run simulation
print("\n🏃 Running simulation...")
simulator = RealtimeSimulatorV2(session_df, model)
results_df = simulator.run_comparison(n_days=13)

print(f"\n✓ Generated {len(results_df)} results")

# Save results
results_df.to_csv('/mnt/user-data/outputs/realtime_simulation_results_v2.csv', index=False)
print("✓ Saved realtime_simulation_results_v2.csv")

#==============================================================================
# ANALYSIS
#==============================================================================

print("\n" + "="*80)
print("SUMMARY RESULTS")
print("="*80)

summary = results_df.groupby('strategy').agg({
    'blocking_rate': 'mean',
    'order_rate': 'mean',
    'delivery_fee_per_session': 'mean',
    'total_value_per_session': 'mean',
    'delivery_fee_per_order': 'mean',
    'total_value_per_order': 'mean'
}).round(4)

print("\n📊 DELIVERY FEE REVENUE (Pricing Optimization Metric)")
print(summary[['blocking_rate', 'order_rate', 'delivery_fee_per_session', 'delivery_fee_per_order']])

print("\n💰 TOTAL ORDER VALUE (Business Revenue Metric)")
print(summary[['blocking_rate', 'order_rate', 'total_value_per_session', 'total_value_per_order']])

# Save summary
summary.to_csv('/mnt/user-data/outputs/realtime_simulation_summary_v2.csv')
print("\n✓ Saved realtime_simulation_summary_v2.csv")

#==============================================================================
# DETAILED COMPARISON
#==============================================================================

print("\n" + "="*80)
print("DETAILED STRATEGY COMPARISON")
print("="*80)

for strategy in ['baseline', 'realtime', 'low', 'high']:
    strat_data = summary.loc[strategy]
    print(f"\n{strategy.upper()}:")
    print(f"  Blocking Rate:           {strat_data['blocking_rate']:.2%}")
    print(f"  Order Rate:              {strat_data['order_rate']:.2%}")
    print(f"  ───────────────────────────────────────")
    print(f"  Delivery Fee/Session:    ${strat_data['delivery_fee_per_session']:.2f}")
    print(f"  Delivery Fee/Order:      ${strat_data['delivery_fee_per_order']:.2f}")
    print(f"  ───────────────────────────────────────")
    print(f"  Total Value/Session:     ${strat_data['total_value_per_session']:.2f}")
    print(f"  Total Value/Order:       ${strat_data['total_value_per_order']:.2f}")

#==============================================================================
# BASELINE VS REALTIME COMPARISON
#==============================================================================

baseline = summary.loc['baseline']
realtime = summary.loc['realtime']

print("\n" + "="*80)
print("REALTIME vs BASELINE COMPARISON")
print("="*80)

blocking_pct = (realtime['blocking_rate'] / baseline['blocking_rate'] - 1) * 100
order_pct = (realtime['order_rate'] / baseline['order_rate'] - 1) * 100
delivery_fee_pct = (realtime['delivery_fee_per_session'] / baseline['delivery_fee_per_session'] - 1) * 100
total_value_pct = (realtime['total_value_per_session'] / baseline['total_value_per_session'] - 1) * 100

print(f"\n📈 Key Metrics:")
print(f"  Blocking Rate:     {baseline['blocking_rate']:.2%} → {realtime['blocking_rate']:.2%} ({blocking_pct:+.1f}%)")
print(f"  Order Rate:        {baseline['order_rate']:.2%} → {realtime['order_rate']:.2%} ({order_pct:+.1f}%)")
print(f"\n💵 Delivery Fee Revenue (What We're Optimizing):")
print(f"  Per Session:       ${baseline['delivery_fee_per_session']:.2f} → ${realtime['delivery_fee_per_session']:.2f} ({delivery_fee_pct:+.1f}%)")
print(f"  Per Order:         ${baseline['delivery_fee_per_order']:.2f} → ${realtime['delivery_fee_per_order']:.2f}")
print(f"\n💰 Total Order Value (Business Impact):")
print(f"  Per Session:       ${baseline['total_value_per_session']:.2f} → ${realtime['total_value_per_session']:.2f} ({total_value_pct:+.1f}%)")
print(f"  Per Order:         ${baseline['total_value_per_order']:.2f} → ${realtime['total_value_per_order']:.2f}")

#==============================================================================
# VISUALIZATION: DELIVERY FEE REVENUE PLOTS
#==============================================================================

print("\n" + "="*80)
print("GENERATING DELIVERY FEE REVENUE PLOTS...")
print("="*80)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Delivery Fee Revenue Plots
metrics_delivery = ['blocking_rate', 'order_rate', 'delivery_fee_per_session']
titles_delivery = ['Blocking Rate', 'Order Rate', 'Delivery Fee Revenue per Session']
colors = ['#e74c3c', '#2ecc71', '#3498db']

for idx, (metric, title, color) in enumerate(zip(metrics_delivery, titles_delivery, colors)):
    ax = axes[idx]
    means = results_df.groupby('strategy')[metric].mean().sort_values()
    
    bars = ax.bar(range(len(means)), means.values, color=color, alpha=0.7, edgecolor='black', linewidth=1.5)
    
    # Highlight realtime strategy
    if 'realtime' in means.index:
        rt_idx = list(means.index).index('realtime')
        bars[rt_idx].set_color('gold')
        bars[rt_idx].set_edgecolor('darkgreen')
        bars[rt_idx].set_linewidth(3)
    
    ax.set_xticks(range(len(means)))
    ax.set_xticklabels([s.capitalize() for s in means.index], fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for i, v in enumerate(means.values):
        if metric in ['blocking_rate', 'order_rate']:
            label = f'{v:.1%}'
        else:
            label = f'${v:.2f}'
        ax.text(i, v, label, ha='center', va='bottom', fontweight='bold', fontsize=11)

plt.suptitle('Delivery Fee Revenue Analysis (Pricing Optimization)', 
             fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/delivery_fee_revenue_plots_v2.png', dpi=300, bbox_inches='tight')
plt.show()

print("✓ Saved delivery_fee_revenue_plots_v2.png")

#==============================================================================
# VISUALIZATION: TOTAL ORDER VALUE PLOTS
#==============================================================================

print("\n" + "="*80)
print("GENERATING TOTAL ORDER VALUE PLOTS...")
print("="*80)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Total Order Value Plots
metrics_total = ['blocking_rate', 'order_rate', 'total_value_per_session']
titles_total = ['Blocking Rate', 'Order Rate', 'Total Order Value per Session']
colors = ['#e74c3c', '#2ecc71', '#9b59b6']

for idx, (metric, title, color) in enumerate(zip(metrics_total, titles_total, colors)):
    ax = axes[idx]
    means = results_df.groupby('strategy')[metric].mean().sort_values()
    
    bars = ax.bar(range(len(means)), means.values, color=color, alpha=0.7, edgecolor='black', linewidth=1.5)
    
    # Highlight realtime strategy
    if 'realtime' in means.index:
        rt_idx = list(means.index).index('realtime')
        bars[rt_idx].set_color('gold')
        bars[rt_idx].set_edgecolor('darkgreen')
        bars[rt_idx].set_linewidth(3)
    
    ax.set_xticks(range(len(means)))
    ax.set_xticklabels([s.capitalize() for s in means.index], fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for i, v in enumerate(means.values):
        if metric in ['blocking_rate', 'order_rate']:
            label = f'{v:.1%}'
        else:
            label = f'${v:.2f}'
        ax.text(i, v, label, ha='center', va='bottom', fontweight='bold', fontsize=11)

plt.suptitle('Total Order Value Analysis (Business Revenue)', 
             fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/total_order_value_plots_v2.png', dpi=300, bbox_inches='tight')
plt.show()

print("✓ Saved total_order_value_plots_v2.png")

#==============================================================================
# COMBINED COMPARISON PLOT
#==============================================================================

print("\n" + "="*80)
print("GENERATING COMBINED COMPARISON PLOT...")
print("="*80)

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Plot 1: Delivery Fee per Order
ax = axes[0, 0]
metric = 'delivery_fee_per_order'
means = results_df.groupby('strategy')[metric].mean().sort_values()
bars = ax.bar(range(len(means)), means.values, color='#3498db', alpha=0.7, edgecolor='black', linewidth=1.5)
if 'realtime' in means.index:
    rt_idx = list(means.index).index('realtime')
    bars[rt_idx].set_color('gold')
    bars[rt_idx].set_edgecolor('darkgreen')
    bars[rt_idx].set_linewidth(3)
ax.set_xticks(range(len(means)))
ax.set_xticklabels([s.capitalize() for s in means.index], fontsize=11, fontweight='bold')
ax.set_title('Delivery Fee per Order', fontsize=13, fontweight='bold')
ax.set_ylabel('Delivery Fee ($)', fontsize=11)
ax.grid(axis='y', alpha=0.3)
for i, v in enumerate(means.values):
    ax.text(i, v, f'${v:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=10)

# Plot 2: Total Value per Order
ax = axes[0, 1]
metric = 'total_value_per_order'
means = results_df.groupby('strategy')[metric].mean().sort_values()
bars = ax.bar(range(len(means)), means.values, color='#9b59b6', alpha=0.7, edgecolor='black', linewidth=1.5)
if 'realtime' in means.index:
    rt_idx = list(means.index).index('realtime')
    bars[rt_idx].set_color('gold')
    bars[rt_idx].set_edgecolor('darkgreen')
    bars[rt_idx].set_linewidth(3)
ax.set_xticks(range(len(means)))
ax.set_xticklabels([s.capitalize() for s in means.index], fontsize=11, fontweight='bold')
ax.set_title('Total Order Value per Order', fontsize=13, fontweight='bold')
ax.set_ylabel('Total Value ($)', fontsize=11)
ax.grid(axis='y', alpha=0.3)
for i, v in enumerate(means.values):
    ax.text(i, v, f'${v:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=10)

# Plot 3: Delivery Fee per Session
ax = axes[1, 0]
metric = 'delivery_fee_per_session'
means = results_df.groupby('strategy')[metric].mean().sort_values()
bars = ax.bar(range(len(means)), means.values, color='#3498db', alpha=0.7, edgecolor='black', linewidth=1.5)
if 'realtime' in means.index:
    rt_idx = list(means.index).index('realtime')
    bars[rt_idx].set_color('gold')
    bars[rt_idx].set_edgecolor('darkgreen')
    bars[rt_idx].set_linewidth(3)
ax.set_xticks(range(len(means)))
ax.set_xticklabels([s.capitalize() for s in means.index], fontsize=11, fontweight='bold')
ax.set_title('Delivery Fee Revenue per Session', fontsize=13, fontweight='bold')
ax.set_ylabel('Revenue ($)', fontsize=11)
ax.grid(axis='y', alpha=0.3)
for i, v in enumerate(means.values):
    ax.text(i, v, f'${v:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=10)

# Plot 4: Total Value per Session  
ax = axes[1, 1]
metric = 'total_value_per_session'
means = results_df.groupby('strategy')[metric].mean().sort_values()
bars = ax.bar(range(len(means)), means.values, color='#9b59b6', alpha=0.7, edgecolor='black', linewidth=1.5)
if 'realtime' in means.index:
    rt_idx = list(means.index).index('realtime')
    bars[rt_idx].set_color('gold')
    bars[rt_idx].set_edgecolor('darkgreen')
    bars[rt_idx].set_linewidth(3)
ax.set_xticks(range(len(means)))
ax.set_xticklabels([s.capitalize() for s in means.index], fontsize=11, fontweight='bold')
ax.set_title('Total Order Value per Session', fontsize=13, fontweight='bold')
ax.set_ylabel('Total Value ($)', fontsize=11)
ax.grid(axis='y', alpha=0.3)
for i, v in enumerate(means.values):
    ax.text(i, v, f'${v:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=10)

plt.suptitle('Delivery Fee vs Total Order Value: Complete Comparison', 
             fontsize=17, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/combined_revenue_comparison_v2.png', dpi=300, bbox_inches='tight')
plt.show()

print("✓ Saved combined_revenue_comparison_v2.png")

#==============================================================================
# FINAL SUMMARY
#==============================================================================

print("\n" + "="*80)
print("SIMULATION COMPLETE!")
print("="*80)

print("\n📁 Generated Files:")
print("  ✓ realtime_simulation_results_v2.csv")
print("  ✓ realtime_simulation_summary_v2.csv")
print("  ✓ delivery_fee_revenue_plots_v2.png")
print("  ✓ total_order_value_plots_v2.png")
print("  ✓ combined_revenue_comparison_v2.png")

print("\n🎯 Key Findings:")
print(f"  Baseline delivery fee/session:  ${baseline['delivery_fee_per_session']:.2f}")
print(f"  Realtime delivery fee/session:  ${realtime['delivery_fee_per_session']:.2f} ({delivery_fee_pct:+.1f}%)")
print(f"  Baseline total value/session:   ${baseline['total_value_per_session']:.2f}")
print(f"  Realtime total value/session:   ${realtime['total_value_per_session']:.2f} ({total_value_pct:+.1f}%)")

print("\n" + "="*80)
