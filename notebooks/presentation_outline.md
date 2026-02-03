# Zipline Dynamic Pricing - Presentation Outline
## 15-Minute Presentation to Executives

---

## SLIDE 1: The Problem (2 min)

### Current State
- **Peak hours**: Customers getting blocked → terrible CX, lost revenue
- **Off-peak hours**: Drones sitting idle → expensive, inefficient
- **Root cause**: Fixed capacity + variable demand + random pricing

### The Dilemma
```
Block customers (bad CX) ←→ Idle assets (high cost)
```

### Our Data Confirms
- Hubs 0-4: 8-12% blocking rate during peak
- First-time users blocked → 20% less likely to become loyal
- Heavy users get blocked most (rejecting best customers!)

**Bottom line**: We need demand management, not capacity rationing.

---

## SLIDE 2: The Solution (3 min)

### Simple Dynamic Pricing Model

**Core Logic in One Sentence:**
> "Raise prices when capacity is tight to prevent blocking; lower prices when capacity is available to reduce idle time."

### How It Works
```
Real-time capacity monitoring
         ↓
    < 50% util  → Discount (attract demand)
    50-70% util → Base price (healthy)
    70-85% util → Moderate surge
    85%+ util   → Strong surge (prevent blocking!)
```

### Key Features
1. **Transparent**: Every price is explainable
2. **Fair**: Responds to real capacity constraints
3. **Market-competitive**: Stays within industry ranges
4. **Differentiated by order type**:
   - Pharma: Higher prices (urgent, inelastic)
   - Meals: Moderate prices
   - Grocery: Lower prices (price-sensitive)

### Example Pricing
| Utilization | Grocery | Meal  | Pharma |
|-------------|---------|-------|--------|
| 30%         | $2.79   | $3.49 | $4.89  |
| 70%         | $4.39   | $5.79 | $8.19  |
| 90%         | $9.99   | $12.99| $16.99 |

---

## SLIDE 3: Why This Beats Alternatives (3 min)

### We Considered Three Approaches

| Approach | Pros | Cons | Verdict |
|----------|------|------|---------|
| **Complex ML Model** | Potentially optimal | Black box, hard to explain, brittle | ❌ Too risky |
| **Fixed Low Price** | Simple, great CX | Revenue loss, doesn't prevent blocking | ❌ Doesn't solve problem |
| **Fixed High Price** | Maximizes revenue | Kills volume, terrible CX | ❌ Wrong priorities |
| **Dynamic (Ours)** | Transparent, addresses all priorities | Requires real-time data | ✅ Best fit |

### Why Simple Rules > Complex ML
- **Explainable**: "It's lunch hour at 90% capacity" not "the model said so"
- **Tunable**: Can adjust thresholds based on business goals
- **Robust**: No model drift, retraining, or mysterious failures
- **Trustworthy**: Executives and customers can understand the logic

### Industry Precedent
- Uber: Surge pricing during peak demand ✓
- Airlines: Dynamic pricing based on capacity ✓
- Hotels: Weekend/event premium pricing ✓

This is proven economics, not experimentation.

---

## SLIDE 4: Expected Impact (4 min)

### Simulated Results (30-day test)

| Metric | Baseline | Dynamic | Improvement |
|--------|----------|---------|-------------|
| **Blocking Rate** | 8.0% | 2.5% | **-69%** ✅ |
| **Revenue/Session** | $1.80 | $2.10 | **+17%** ✅ |
| **Capacity Variance** | 0.25 | 0.18 | **-28%** ✅ |

### Translating to Business Impact

**Priority 1: Customer Experience** ✅
- 5.5% reduction in blocking = ~1,650 fewer blocked sessions/month
- Protected first impressions (critical for retention)
- No more "unavailable" message - customers see a price and decide

**Priority 2: Profit** ✅
- 17% revenue increase = ~$45K additional revenue/month (at current scale)
- Captured willingness-to-pay during peak demand
- Better margins on inelastic demand (Pharma)

**Priority 3: Asset Utilization** ✅
- 28% smoother capacity usage = more predictable operations
- Reduced idle time = better ROI on drone fleet
- Fewer emergency capacity adjustments

### What About Customer Pushback?

**Expected**: Some price complaints during surge
**Reality**: Customers prefer transparent pricing over blocking
**Mitigation**: 
- Clear messaging: "High demand right now, delivery in 20 min" 
- Off-peak discounts encourage shifting behavior
- Still competitive with market (DoorDash surges to $15-25)

---

## SLIDE 5: Implementation Plan (3 min)

### Phase 1: Soft Launch (Weeks 1-2)
- Deploy at 3 high-blocking hubs (0, 1, 3)
- A/B test: 50% dynamic, 50% baseline
- **Success criteria**: Blocking rate < 4%

### Phase 2: Optimization (Weeks 3-4)
- Tune thresholds based on results
- Adjust price caps if needed
- Gather customer feedback

### Phase 3: Full Rollout (Week 5+)
- Deploy to all 15 hubs
- Build real-time monitoring dashboard
- Continuous optimization

### What We Need
- **Engineering**: Real-time capacity tracking (2 weeks)
- **Marketing**: Customer communication plan (1 week)
- **Analytics**: Dashboard for monitoring (1 week)
- **Total timeline**: 6 weeks to full rollout

### Risk Mitigation
- **Kill switch**: Can revert to baseline instantly if issues
- **Gradual rollout**: Prove it works at 3 hubs before expanding
- **Conservative thresholds**: Start with higher blocking threshold (90%) if needed

---

## BACKUP SLIDES (If Time Allows / Q&A)

### Technical Details
- Capacity calculation methodology
- Elasticity estimates by order type
- Distance-based adjustments
- Price ceiling rationale

### Alternative Scenarios Tested
- What if we only surge Pharma? (Misses grocery opportunity)
- What if we use hourly price updates? (Too slow, still get blocking)
- What if we charge per mile? (Doesn't address capacity)

### Long-term Enhancements
- Machine learning for demand forecasting
- Personalized pricing (loyalty discounts)
- Integration with promotional campaigns
- Multi-hub route optimization

---

## ANTICIPATED QUESTIONS & ANSWERS

### Q: "Why not just buy more drones?"
A: Capital expense of $X million vs. operational change of $0. Plus, more drones means higher fixed costs during off-peak. Better to optimize what we have first.

### Q: "Won't high prices hurt our brand?"
A: Industry standard (Uber, DoorDash). Plus, we're preventing blocking which is MUCH worse for brand. Customers understand "busy = expensive" better than "busy = unavailable".

### Q: "How do we know the elasticity estimates are correct?"
A: Derived from your own data (30 days of random pricing). We saw real conversion rates at different price points. Can refine with A/B testing.

### Q: "What if competitors undercut us during peak?"
A: They'll face the same capacity constraints. If they block customers, we win on CX. If they somehow have unlimited capacity, we can adjust our thresholds.

### Q: "Can we customize by hub?"
A: Yes! Model allows hub-specific parameters. Can set different thresholds for high-blocking hubs (0-4) vs. well-performing hubs (12-14).

### Q: "What about weather/events causing sudden demand spikes?"
A: Model responds in real-time to actual capacity utilization. Demand spike → higher utilization → higher prices → demand throttled. Automatic.

### Q: "How do we explain this to customers?"
A: Simple message: "High demand right now. Order now for $12.99 or schedule for later at $4.99." Gives choice, doesn't block.

---

## RECOMMENDED TALKING POINTS

### Opening Hook
"What's worse: Telling a customer the price is $15, or telling them we can't serve them at all? Our data shows blocking a first-time customer costs us 20% probability they become loyal. That's the real cost we're optimizing against."

### Confidence Builders
- "This is proven economics, not experimentation - Uber, airlines, hotels all use capacity-based pricing"
- "We can revert instantly if it doesn't work - there's a kill switch"
- "We're starting with just 3 hubs to prove it before full rollout"

### Closing Strong
"Dynamic pricing isn't about squeezing customers - it's about making sure we CAN serve them when they need us. By preventing blocking, we protect our brand, our customers, and our revenue. And we do it with a simple, transparent system that everyone can understand."

---

## PRESENTATION STYLE NOTES

### DO:
- Lead with customer impact (Priority 1)
- Use concrete numbers ($45K revenue, 1,650 fewer blocks)
- Acknowledge risks and show mitigation plans
- Invite skepticism ("What concerns you most about this?")

### DON'T:
- Get too technical about algorithms
- Oversell or sound defensive
- Ignore the "customer pushback" elephant in the room
- Present as fait accompli - it's a proposal seeking buy-in

### TONE:
- Confident but humble
- Data-driven but customer-focused
- Acknowledging complexity while presenting simplicity
