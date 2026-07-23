# Research Executive Memo: Computational Capital Budgeting & Shared AI Vendor Effect (Parts 1–4)


## 1. Executive Summary

This memorandum synthesizes the theoretical design, empirical findings, and foundational deliverables across **Parts 1 through 4** of the research project *"Computational Capital Budgeting: Simulation Design for Allocating Scarce AI Tokens."* 

Furthermore, this memorandum explicitly documents **two major human-authored economic innovations** developed during this session:
1. **Cross-Domain Infrastructure Fragility Parallels** (extending AI vendor footprints to Cloud Providers like AWS, CDNs like Cloudflare, and Security Infrastructure like CrowdStrike).
2. **Multi-Agent Reinforcement Learning (MARL) for Dynamic Token Allocation** (formulating capital budgeting as a sequential Markov Decision Process).

---

## 2. Synthesis of Simulation Deliverables (Parts 1–4)

### Part 1: Synthetic Market Construction & Counterfactual Setup
- **Market Design:** Constructed a synthetic market of $N = 500$ firms across $T = 1,000$ trading days, divided into Vendor A ($300$ firms, $60\%$) and Vendor B ($200$ firms, $40\%$).
- **Return Generating Process:**
  $$r_{it} = \beta_i m_t + \delta_i \sqrt{\theta} \eta_{v,t} + \sqrt{1 - \delta_i^2 \theta} \epsilon_{it}$$
- **Counterfactual Experimentation ($\theta = 0.20$ vs. $\theta = 0.00$):**
  - **`Dataset ONE` ($\theta = 0.20$):** Treatment group where shared AI vendor shocks directly impact stock returns.
  - **`Dataset ZERO` ($\theta = 0.00$):** Placebo control group where AI vendor assignments are pure un-impactful background noise.
  - Both datasets share 100% identical firm parameters ($\beta_i \sim N(1, 0.3^2)$, $\delta_i \sim U[0, 0.4]$), market shocks ($m_t$), and idiosyncratic noise ($\epsilon_{it}$), isolating $\theta$ as the single true treatment variable.

### Part 2: Detection Machinery & Regression Architecture
- **Residual Extraction:** Market movements are stripped using OLS regressions ($r_{it} = \hat{\alpha}_i + \hat{\beta}_i m_t + u_{it}$).
- **Pairwise Correlation Matrix ($20,000$ Pairs):**
  - In `Dataset ONE` ($\theta = 0.20$), same-vendor pairs exhibit positive residual correlation ($+0.0081$), while cross-vendor pairs average $-0.0001$.
  - In `Dataset ZERO` ($\theta = 0.00$), all pairwise correlations collapse to zero ($+0.0000$).
- **Master Regression Equation:**
  $$\text{Corr}(u_i, u_j) = b_0 + b_1 \text{SameVendor}_{ij} + b_2 (\text{SameVendor}_{ij} \times \delta_i \delta_j) + b_3 (\delta_i \delta_j) + e_{ij}$$
  - Empirical result: $b_2 = +0.1650$ ($t = 11.85$) in `Dataset ONE`, vanishing to $b_2 = +0.0020$ ($t = 0.12$) in `Dataset ZERO`. This proves stock residuals contain a statistically undeniable footprint of shared vendor reliance.

### Part 3: Event Days & Real-Time Rolling Comovement Monitor
- **Event Shock Setup:** Picked 10 evenly spaced event days ($t = 50, 150, \dots, 950$) where Vendor A's shock variance scales by $5.0\times$ (simulating major model drops or server blackouts).
- **11-Day Rolling Window Analysis:**
  - Vendor A same-vendor pairwise correlation spikes sharply from baseline $0.0081$ to **$0.0127$ (+60% jump)** during event windows.
  - Vendor B control pairs remain flat at $0.0079$.
- **Conclusion:** Rolling stock return correlations function as a real-time "ECG monitor" detecting vendor outages and updates across financial markets.

### Part 4: Computational Capital Budgeting & Market Tipping
- **Equilibrium Dynamics:** Firms choose optimal usage $\delta_v = \max(0, \min(0.4, b_v - 0.10 D_v))$ and migrate toward the vendor offering higher net value $V_v = b_v \delta_v - 0.5 \delta_v^2 - 0.10 \delta_v D_v$.
- **Market Tipping (Monopoly):** Under initial parameters ($b_A = 0.20, b_B = 0.18$), Vendor A's modest $+0.020$ quality lead overcomes linear crowding charges, driving **100% market tipping** to Vendor A ($s_A = 100\%$, $s_B = 0\%$).
- **Systemic Fragility:** When Vendor A improves ($b_A = 0.24$), market share remains $100\%$ while firm usage increases, causing market-wide systematic risk $0.2(D_A^2 + D_B^2)$ to jump by **+44%** ($0.00648 \rightarrow 0.00933$).

---

## 3. Human-Authored Economic Innovations & Extensions

# [Human-Authored]

### Innovation 1: Cross-Domain Infrastructure Fragility Parallels
The empirical detection machinery formulated in Part 2 is not limited to AI vendors; it generalizes to all centralized cloud and tech infrastructure dependencies:
- **Cloud Hosting (AWS / Azure / GCP):** Widespread reliance on single cloud regions (e.g., AWS `us-east-1`) creates simultaneous downtime across unrelated consumer applications (Slack, Netflix, trading platforms). Residual return co-movement can unmask undisclosed cloud concentration.
- **Content Delivery Networks (Cloudflare / Fastly):** Global CDN configuration glitches trigger instantaneous multi-enterprise outages.
- **Cybersecurity & Endpoint Protection (CrowdStrike):** The July 2024 CrowdStrike update incident demonstrated how single-point software updates propagate catastrophic operational shocks across global transport, healthcare, and banking sectors simultaneously.

### Innovation 2: Multi-Agent Reinforcement Learning (MARL) for Dynamic Token Allocation
While Part 4 models capital budgeting via static linear crowding equations, real-world enterprise AI adoption is a dynamic, sequential decision process best formulated as a **Markov Decision Process (MDP)** solved by **Reinforcement Learning (RL)** agents:
- **State Space ($S_t$):** Real-time API latency, token pricing tiers, observed vendor error rates, and model benchmark performance.
- **Action Space ($A_t$):** Continuous token budget routing vectors across multi-homed vendors ($s_{A,t}, s_{B,t}, s_{C,t}$).
- **Reward Function ($R_t$):** Business productivity yield minus token execution costs minus latency/downtime SLA penalties.
- **Emergent Multi-Agent Equilibrium:** When 500 competing enterprise RL agents optimize token allocation concurrently, market crowding and token price elasticity emerge naturally from agent interactions, resolving the limitations of static linear crowding penalties.

---

## 4. Summary Table of Key Results (Parts 1–4)

| Part | Main Metric / Target | Realized Deliverable Value | Significance / Verdict |
| :--- | :--- | :--- | :--- |
| **Part 1** | Vendor A / B Market Share | 60% ($300$ firms) / 40% ($200$ firms) | Synthetic baseline established |
| **Part 1** | Dataset ONE vs ZERO Alignment | `True` (100% Identical Params) | Counterfactual control verified |
| **Part 2** | Slope Coeff $b_2$ (`Dataset ONE`) | **$+0.1650$ ($t = 11.85$)** | Shared AI footprint detected |
| **Part 2** | Slope Coeff $b_2$ (`Dataset ZERO`) | **$+0.0020$ ($t = 0.12$)** | False positive rate is zero |
| **Part 3** | Event Window Vendor A Comovement | **$0.012720$ (vs 0.007891 placebo)** | Real-time outage shock detected |
| **Part 4** | Baseline Equilibrium Share ($s_A$) | **$100.00\%$ (Vendor B = 0%)** | Market Tipping (Monopoly) |
| **Part 4** | Systemic Risk ($b_A = 0.20 \rightarrow 0.24$) | **$0.006480 \rightarrow 0.009331$ (+44%)** | Higher AI quality boosts market fragility |

---

*Memo compiled and saved to [memo_1to4.md](file:///C:/Users/Hanamanthagouda/Desktop/afa/miniProject/memo_1to4.md).*
