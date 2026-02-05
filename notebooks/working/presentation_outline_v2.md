# Dynamic Pricing Presentation Outline
**Audience:** Solutions Engineer (Hiring Manager), Data Platform Engineer, VP of Marketing  
**Duration:** 15-minute presentation + 20-minute Q&A  
**Date:** [Your Interview Date]

---

## Presentation Strategy

### Audience Analysis:
- **Solutions Engineer (Hiring Manager)**: Wants to see problem-solving, technical depth, communication skills
- **Data Platform Engineer**: Interested in implementation feasibility, data requirements, technical architecture
- **VP of Marketing**: Cares about customer impact, brand risk, competitive positioning, go-to-market

### Key Message:
"We can reduce blocking 62% and increase revenue 69% while protecting our most valuable customer segments through real-time capacity-based pricing with customer tier protection."

---

## SLIDE 1: The Problem (2 minutes)

**Title:** "Blocking Costs Us High-Value Customers"

### Visual Elements:
- Two-bar comparison: First order success (95% loyal) vs First order blocked (74% loyal)
- Current state box: 22% blocking rate, random impact
- Business impact callout: Lost LTV, competitive vulnerability, NPS risk

### Key Talking Points:
1. **Open strong**: "We have a 22% blocking rate. That's not just lost revenue—it's lost relationships."
2. **The insight**: "Our data shows first-order success drives 95% loyalty vs 74% if blocked. That's a 21 percentage point gap."
3. **The cost**: "We're randomly blocking everyone, including first-timers and loyal customers—our most valuable segments."
4. **Why now**: "Peak demand causes blocking. Off-peak we have idle assets. We need intelligent demand management."

### Audience-Specific Emphasis:
- **Solutions Engineer**: Problem-solving approach, data-driven insight
- **Data Platform Engineer**: Scale of the problem (22% of all sessions)
- **VP Marketing**: Customer lifetime value at stake, brand reputation risk

---

## SLIDE 2: The Insight (2 minutes)

**Title:** "Not All Customers Are Equal"

### Visual Elements:
- Session composition breakdown: 75% Loyal, 8.4% First-timers, 16.7% Occasional
- Price sensitivity data: Pharma (85% convert), Meal (55%→49%), Grocery (43%→35%)
- Key finding callout: Higher prices reduce blocking (5.3%→3.3%)

### Key Talking Points:
1. **The data work**: "We ran a 30-day random pricing test—essentially a natural experiment to measure price sensitivity."
2. **Customer segmentation**: "83% of sessions come from first-timers or loyal users. These are our high-value segments."
3. **The breakthrough**: "We found price CAN reduce blocking without destroying conversion. Pharma users barely care about price. Even Grocery only drops 8 points."
4. **The opportunity**: "Protect high-value segments while using price to intelligently throttle demand."

### Audience-Specific Emphasis:
- **Solutions Engineer**: Analytical rigor, testing methodology
- **Data Platform Engineer**: Data sources used (30-day test), sample sizes
- **VP Marketing**: Customer segmentation, willingness to pay

---

## SLIDE 3: The Solution (4 minutes - HERO SLIDE)

**Title:** "Real-Time Pricing with Customer Protection"

### Visual Elements:
- Left side: 6-tier pricing table (capacity → price multiplier)
- Right side: Customer protection breakdown with tier caps
- Bottom: Competitor pricing benchmark callout

### Key Talking Points:
1. **How it works**: "Six simple capacity thresholds. When we're at 85% capacity, prices surge. When we're at 30% capacity, we discount."
2. **The innovation** (pause for emphasis): "Customer tier protection. First-timers get max 10% surge even at 95% capacity. Loyal users capped at 30% surge."
3. **Who gets protected**: "83% of sessions—first-timers and loyal users—get pricing protection. We throttle the 17% occasional users."
4. **Market positioning**: "We benchmarked competitors. DoorDash and Uber surge to $14-25 with tip. We cap at $12-16. We stay competitive."
5. **Simplicity**: "It's rule-based, not black-box ML. Operators can understand and tune it. Six numbers to adjust."

### Audience-Specific Emphasis:
- **Solutions Engineer**: Elegant solution, balances complexity with interpretability
- **Data Platform Engineer**: Real-time capacity feed requirement, simple logic = easy to implement
- **VP Marketing**: Customer protection, competitive pricing, brand-safe messaging

### Anticipated Questions (prepare for):
- "Why not ML?" → Interpretability, only 30 days data, can layer ML later
- "What if customers complain?" → We're cheaper than competitors, clear messaging
- "How do you identify tiers?" → User ID + session count (simple lookup)

---

## SLIDE 4: Business Impact (4 minutes)

**Title:** "Strategic Trade-offs with Strong Results"

### Visual Elements:
- Three-panel comparison: Blocking Rate, Revenue per Session, Order Rate
- Each panel: Blue bar (Baseline), Green bar (Model), percent change with ✅/⚠️
- Bottom callout: "83% of sessions protected • 17% throttled"

### Key Talking Points:
1. **Lead with wins**: "Blocking reduced 62%. Revenue per session increased 69%. Both priorities achieved."
2. **Address order rate proactively**: "Order rate drops 36%. This is intentional, not accidental."
3. **The reframe**: "Before: 22% blocked randomly, including VIPs. After: 8% blocked at capacity limit, 17% throttled via price—occasional users."
4. **The choice**: "We're CHOOSING who to serve when constrained. That's better than random blocking."
5. **Customer impact**: "First-timers and loyal customers get served reliably. That's what drives long-term growth."

### Audience-Specific Emphasis:
- **Solutions Engineer**: Trade-off analysis, defensible decisions
- **Data Platform Engineer**: Metrics you'll track, monitoring approach
- **VP Marketing**: Customer experience improvement, retention focus, not volume focus

### Handling Pushback:
**If they focus on order rate drop:**
> "The alternative is blocking 22% randomly. That includes first-timers who have only 74% chance of becoming loyal. We're protecting the 83% who matter most and throttling the 17% who are lower value. That's strategic."

---

## SLIDE 5: The Ask (3 minutes)

**Title:** "Recommendation: Phased Rollout"

### Visual Elements:
- Three-phase timeline: Phase 1 (Hubs 0,1,3), Phase 2 (Tune), Phase 3 (Rollout)
- Success metrics box: Blocking <10%, First-timer loyalty >90%, Revenue +50%, NPS maintained
- Requirements box: Real-time capacity feed, User ID tracking, Price lock-in
- Risk mitigation box: Kill switch, Conservative start, A/B test validates

### Key Talking Points:
1. **The recommendation**: "Start at 3 hubs with worst blocking. A/B test for 2 weeks to validate assumptions."
2. **Low risk**: "Kill switch ready. We start conservative and can tune. If it doesn't work, we revert instantly."
3. **Success criteria**: "We'll measure blocking rate, first-timer loyalty, revenue per session, and NPS. Clear go/no-go criteria."
4. **Technical requirements**: "Real-time capacity feed—which drones are flying. User ID tracking for tiers. Price lock-in system—show price, honor for 10 minutes."
5. **Timeline**: "Two weeks to validate, two weeks to optimize, then scale to all 15 hubs."

### The Ask (be direct):
> "I'm recommending we approve Phase 1 deployment at Hubs 0, 1, and 3 with a two-week A/B test. This is low-risk, high-reward. What questions do you have?"

### Audience-Specific Emphasis:
- **Solutions Engineer**: Clear recommendation, execution plan, decision framework
- **Data Platform Engineer**: Technical requirements feasible? Data availability?
- **VP Marketing**: NPS monitoring, customer communication plan, brand protection

---

## Transition to Q&A

**After Slide 5:**
> "That's my recommendation. I know you'll have questions about the methodology, the assumptions, and the implementation. I have my analysis ready to share. What would you like to dig into first?"

---

## Q&A Preparation (20 minutes)

### Have Ready:
1. **Jupyter Notebook** - Open to key sections:
   - Price sensitivity analysis (conversion by price charts)
   - Customer segmentation (loyalty analysis)
   - Simulation methodology
   - Results breakdown by hub

2. **Key Numbers Memorized:**
   - First order: 95% vs 74% loyalty
   - Blocking: 22.1% → 8.5% (-62%)
   - Revenue: $7.97 → $13.51 (+69%)
   - Order rate: 61.5% → 39.6% (-36%)
   - Customer protection: 83% (75% loyal + 8% first-timers)
   - Competitor pricing: $14-25 (we cap at $12-16)
   - Elasticity: Pharma -0.05, Meal -0.20, Grocery -0.30

### Likely Questions by Audience Member:

#### Solutions Engineer (Hiring Manager):
**Q: "Walk me through how you approached this problem."**
> "Started with exploratory analysis—what causes blocking? Found it correlates with hub capacity. Then analyzed customer segments—discovered first-order success drives 21-point loyalty gap. That became the key insight: protect valuable segments. Built simulation to test, validated with calibrated elasticity from the 30-day pricing test."

**Q: "What alternatives did you consider?"**
> "Three main alternatives: Time-based pricing—too rigid, Friday 6pm looks different than Sunday 6pm. ML demand forecasting—black box, only 30 days of data. Uniform surge—hurts valuable customers equally. I chose real-time capacity because it's simple, interpretable, and responds to actual demand."

**Q: "How confident are you in these results?"**
> "Moderately confident. The elasticity estimates are based on real data. The simulation logic is sound. But simulation isn't reality—that's why Phase 1 is an A/B test. I've made conservative assumptions. The model is tunable if we're wrong."

**Q: "What would make you change your recommendation?"**
> "If the A/B test shows: First-timer loyalty drops, NPS declines significantly, or competitor responses that threaten market share. Those would trigger either tuning the caps down or killing the test."

#### Data Platform Engineer:
**Q: "What data infrastructure do you need?"**
> "Three things: Real-time capacity feed—which drones are flying right now, updates every 30 seconds. User ID to session mapping—for tier identification. Price lock-in system—show price, store it, honor for 10 minutes even if capacity changes."

**Q: "How do you calculate real-time utilization?"**
> "Track active deliveries per hub. Each order starts with flight time = (distance/70mph)*60 + 5 minutes fixed time. Mark drone busy, set return timestamp. Current utilization = active drones / total capacity. Simple state tracking."

**Q: "What's the latency requirement?"**
> "Capacity updates every 30 seconds is fine. Pricing calculation is <10ms—it's just a lookup table and multiplication. Price lock-in prevents price changes during user session. Not high-latency sensitive."

**Q: "How does this scale to 100 hubs?"**
> "Linear scaling. Each hub's utilization is independent. No complex dependencies. The pricing logic is stateless—just input current utilization, output price. Could handle 1000 hubs with same architecture."

**Q: "What about data quality issues?"**
> "Two failure modes: Drone status feed goes down → default to base pricing (safe fallback). User ID missing → treat as unknown tier (full surge). Graceful degradation built in. Monitor feed health as key operational metric."

#### VP of Marketing:
**Q: "How will customers react to surge pricing?"**
> "We benchmarked competitors—we're actually LOWER than DoorDash/Uber. Plus we protect first-timers and loyal users, so 83% of customers rarely see aggressive surge. We show clear messaging: 'High demand right now' vs just 'Unavailable.' Price transparency beats blocking."

**Q: "What's the messaging strategy?"**
> "Three pillars: Transparency ('Prices vary by demand'), Fairness ('Same capacity = same price'), Value ('Skip the wait, get reliable delivery'). We lead with reliability, not cheapness. For first-timers: 'Welcome pricing' to reinforce protection."

**Q: "What if competitors undercut us?"**
> "We monitor weekly. If they drop prices below ours at peak, we have two options: Adjust our surge caps down (tunable), or lean into reliability messaging—'We deliver when others block you.' Our advantage is availability, not just price."

**Q: "How does this affect NPS?"**
> "That's our key risk metric in Phase 1. We expect neutral-to-positive NPS impact because: Blocking is worse than surge for NPS, we're protecting our best customers, and we're still competitive with market. If NPS drops >5 points, we kill or tune."

**Q: "What about brand perception?"**
> "We frame it as 'reliable delivery' not 'surge pricing.' The narrative is: 'We ensure you can always order.' First-timers get protected pricing—that's their brand impression. Loyal customers get better treatment than occasional users—that's brand loyalty signal."

**Q: "How do we communicate this to customers?"**
> "In-app: Simple pricing explanation page. FAQ: 'Why does pricing vary?' Customer service: Scripts for complaints. Social: Reliability messaging, not price messaging. We emphasize availability, not dynamic pricing. Customers care more about 'can I order?' than '$1 difference.'"

### Wild Card Questions:

**Q: "What if you're completely wrong about elasticity?"**
> "That's why we A/B test. If elasticity is higher than estimated, we'll see order rate drop more than simulated. We tune caps down—maybe first-timers get 5% max instead of 10%. Model is designed to be adjustable. We learn and iterate."

**Q: "How long until we see ROI?"**
> "Revenue impact is immediate—we see it in week 1 of Phase 1. Customer retention impact takes 3 months to measure properly. But blocking reduction happens day 1. I'd expect positive ROI within first month of full rollout."

**Q: "Why not just buy more drones?"**
> "Capital expense of $XXX million vs. tuning pricing. Drones would sit idle off-peak—making the asset utilization problem worse. Dynamic pricing solves both peak blocking AND off-peak idle capacity. It's the elegant solution."

**Q: "What happens during a major event? Super Bowl, etc."**
> "Extreme demand events are interesting. Options: Cap surge at lower multiplier to avoid gouging perception, or allow higher surge with clear messaging. I'd recommend event-specific overrides—we can manually adjust caps for known major events. Monitor social sentiment in real-time."

---

## Closing

**After Q&A:**
> "Thank you for the thoughtful questions. I believe this approach balances customer experience, profitability, and operational simplicity. I'm excited about the opportunity to implement this at Zipline and iterate based on real-world results. What are next steps?"

---

## Backup Materials

### If They Want to See Code:
- Open `realtime_capacity_simulation.ipynb`
- Show simulation logic (chronological processing, utilization tracking)
- Show pricing function (clean, simple)
- Show customer tier protection logic

### If They Want More Data Analysis:
- Show price sensitivity charts (conversion by price bins)
- Show hub performance breakdown (blocking by hub)
- Show customer lifetime value analysis (loyal vs occasional)

### If They Challenge Order Rate Drop Further:
- Show alternative scenario: "If we kept blocking at 22%, we'd lose MORE customer LTV than throttling 17% occasional users"
- Pull up customer tier breakdown: "Which 17% do you want to turn away? We chose lowest-value segment"

---

## Success Criteria for This Presentation

You'll know you nailed it if:
1. ✅ They ask about **implementation details** (means they're bought in)
2. ✅ They discuss **Phase 1 timeline** (means they're planning to move forward)
3. ✅ They ask **"What do you need from us?"** (means you're in the driver's seat)
4. ✅ VP Marketing asks about **messaging strategy** (means they're thinking about go-to-market)
5. ✅ Data Engineer asks about **data schema** (means they're planning integration)

You'll know you didn't land it if:
1. ❌ They go back to Slide 1 repeatedly (means unclear problem)
2. ❌ They challenge assumptions without asking to see data (means they don't trust you)
3. ❌ They ask "What else did you consider?" multiple times (means they think you jumped to conclusions)
4. ❌ Dead silence after Slide 5 (means you didn't inspire confidence)

---

## Final Reminders

### Do:
- Lead with business impact (LTV, not just metrics)
- Show, don't tell (pull up charts when questioned)
- Own the trade-offs (order rate drop is strategic)
- Be specific about implementation (show you've thought it through)
- Make a clear ask (approve Phase 1)

### Don't:
- Apologize for order rate drop (frame as trade-off)
- Get defensive about limitations (acknowledge and mitigate)
- Rush through Slide 3 (your hero slide—take your time)
- Wing the Q&A (know your numbers cold)
- End weakly (clear ask, strong close)

### Your Differentiator:
"I didn't just build a model. I solved a business problem with a practical solution that protects customers, increases revenue, and can be deployed in 2 weeks. And I have a plan to learn and iterate."

**You've got this.** 🚀
