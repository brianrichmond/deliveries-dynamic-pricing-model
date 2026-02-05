# ONE-LINE FIX for Revenue Calculation Bug

## The Problem
Line 276 in your notebook adds delivery_fee + subtotal, giving you total order value (~$30/order) instead of delivery fee revenue (~$3.53/order).

## The Fix

### BEFORE (Line 276):
```python
revenue = float(price) + float(subtotal) if pd.notna(price) and pd.notna(subtotal) else 0.0
```

### AFTER (Line 276):
```python
delivery_fee_revenue = float(price) if pd.notna(price) else 0.0
```

## Additional Changes Needed

Since you're changing `revenue` to `delivery_fee_revenue`, you'll need to update a few other lines:

### Line 332 (in simulate_day method):
**BEFORE:**
```python
total_revenue = sum(r['revenue'] for r in all_results)
```

**AFTER:**
```python
total_delivery_fee_revenue = sum(r['delivery_fee_revenue'] for r in all_results)
```

### Line 340 (in simulate_day return):
**BEFORE:**
```python
'revenue': float(total_revenue),
```

**AFTER:**
```python
'delivery_fee_revenue': float(total_delivery_fee_revenue),
```

### Line 343 (in simulate_day return):
**BEFORE:**
```python
'revenue_per_session': float(total_revenue / total_sessions) if total_sessions > 0 else 0.0
```

**AFTER:**
```python
'delivery_fee_per_order': float(total_delivery_fee_revenue / total_orders) if total_orders > 0 else 0.0,
'delivery_fee_per_session': float(total_delivery_fee_revenue / total_sessions) if total_sessions > 0 else 0.0
```

## Expected Results After Fix

Once you make these changes and re-run the simulation, you should see:

### Baseline Strategy
- Delivery fee per order: **~$3.53** ✓ (matches original data)
- Delivery fee per session: **~$1.80-2.10** ✓ (matches original data)
- Order rate: **50-60%**

### Realtime Strategy  
- Delivery fee per order: **$5-10** (mix of discounts and surges)
- Delivery fee per session: **$2.50-4.00** (higher than baseline)
- Order rate: **40-50%** (lower due to surge pricing)

### Low Strategy ($2.99 fixed)
- Delivery fee per order: **~$2.99**
- Delivery fee per session: **~$1.80-2.10**
- Order rate: **60-70%** (higher due to low price)

### High Strategy ($12.99 fixed)
- Delivery fee per order: **~$12.99**
- Delivery fee per session: **~$2.60-3.90**
- Order rate: **20-30%** (much lower due to high price)

## Quick Verification

After making the changes, add this verification cell:

```python
# Verify the fix worked
baseline_results = results_df[results_df['strategy'] == 'baseline']
avg_fee_per_order = baseline_results['delivery_fee_revenue'].sum() / baseline_results['orders'].sum()

print(f"Baseline delivery fee per order: ${avg_fee_per_order:.2f}")
print(f"Expected: ~$3.53")
print(f"Match: {'✓ YES' if 3.0 < avg_fee_per_order < 4.5 else '✗ NO - check your fix'}")
```

If you see ~$3.53, the fix worked! If you still see $12-30, something went wrong.

## Optional: Track Both Metrics

If you want to track BOTH delivery fees and total order value (for business intelligence), you can keep both:

```python
# Line 276-277:
delivery_fee_revenue = float(price) if pd.notna(price) else 0.0
total_order_value = delivery_fee_revenue + float(subtotal) if pd.notna(subtotal) else delivery_fee_revenue

# Return both in the result dict:
return {
    'outcome': outcome,
    'delivery_fee_revenue': delivery_fee_revenue,  # For optimization
    'total_order_value': total_order_value,        # For business metrics
    'price': float(price),
    'utilization': util
}
```

Then you can analyze:
- **Delivery fee revenue**: What you're optimizing with pricing
- **Total order value**: Total business impact (mostly driven by what customers buy, not delivery fees)
