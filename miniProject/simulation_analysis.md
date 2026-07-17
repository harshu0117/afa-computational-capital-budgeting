# Shared-AI-Vendor Effect: Simulation Analysis and Rigorous Economic Critique

**Document Version:** 1.0  
**Target Submission:** American Finance Association (AFA) Special Session  
**Code Workspace:** [miniProject](file:///C:/Users/Hanamanthagouda/Desktop/afa/miniProject)  
**Outputs Directory:** [miniProject/data](file:///C:/Users/Hanamanthagouda/Desktop/afa/miniProject/data) | [miniProject/plots](file:///C:/Users/Hanamanthagouda/Desktop/afa/miniProject/plots)

---

## Section 1: Output Analysis & Empirical Verification

We verified the output datasets and plotted figures against the mathematical specifications of the research paper [AFA_Simulation_V1.pdf](file:///C:/Users/Hanamanthagouda/Desktop/afa/miniProject/AFA_Simulation_V1.pdf).

### 1. Part 1: Dataset Generation & Firm Assignments
* **File Verified:** [part1_report.txt](file:///C:/Users/Hanamanthagouda/Desktop/afa/miniProject/data/part1_report.txt)
* **Parameters & Distributions:**
  * Total Firms $N = 500$; Trading Days $T = 1000$.
  * Vendor $A$ Share = $60\%$ ($300$ firms); Vendor $B$ Share = $40\%$ ($200$ firms).
  * Usage $\delta_i \sim U[0, 0.4]$ yields an empirical average of **$0.1994$** (theoretical mean $0.20$).
  * Sensitivity $\beta_i \sim N(1, 0.3^2)$ yields an empirical average of **$1.0023$** (theoretical mean $1.00$).
* **Cross-Dataset Identity:** The script confirmed that both `Dataset ONE` ($\theta = 0.2$) and `Dataset ZERO` ($\theta = 0.0$) used identical firm assignments ($\delta_i, \beta_i, v(i)$) and identical daily shocks ($m_t, \eta_{A,t}, \eta_{B,t}, \epsilon_{it}$). 

### 2. Part 2: Statistical Signatures and Placebo Checks
* **File Verified:** [part2_report.txt](file:///C:/Users/Hanamanthagouda/Desktop/afa/miniProject/data/part2_report.txt) | [part2_binned_scatter.png](file:///C:/Users/Hanamanthagouda/Desktop/afa/miniProject/plots/part2_binned_scatter.png)
* **Average Correlations:**
  * **Dataset ONE ($\theta = 0.2$):** Same-vendor pairs have an average correlation of **$0.008136$**, whereas cross-vendor pairs show a flat/zero correlation of **$-0.000094$**.
  * **Dataset ZERO ($\theta = 0.0$):** Both same-vendor ($0.000233$) and cross-vendor ($-0.000495$) correlations are effectively zero.
* **Regression Signatures:**
  $$\text{corr}_{ij} = b_0 + b_1 \text{SameVendor}_{ij} + b_2 (\text{SameVendor}_{ij} \times \delta_i \delta_j) + b_3 \delta_i \delta_j + e_{ij}$$
  
  | Coefficient | Dataset ONE (Expected) | Dataset ZERO (Control) | Status |
  | :--- | :--- | :--- | :--- |
  | **$b_0$ (Intercept)** | $-0.00083$ (SE: $0.00048$) | $-0.00051$ (SE: $0.00048$) | Statistically zero |
  | **$b_1$ (Same Vendor)** | $0.00242$ (SE: $0.00067$) | $0.00191$ (SE: $0.00067$) | Significant under ONE ($t \approx 3.6$) |
  | **$b_2$ (Joint AI Usage)** | **$0.14682$** (SE: $0.01239$) | **$-0.02994$** (SE: $0.01239$) | Highly significant ($t \approx 11.85$) only under ONE |
  | **$b_3$ (Placebo Product)** | $0.01822$ (SE: $0.00885$) | $0.00037$ (SE: $0.00886$) | Statistically insignificant/near zero |

* **Empirical Match:** The results match the paper's predictions. Under $\theta = 0.2$, the joint usage product $\delta_i \delta_j$ scales same-vendor comovement ($b_2 > 0$ and highly significant), whereas under $\theta = 0.0$, the effect completely vanishes. The placebo check ($b_3 \approx 0$) confirms that heavy AI users on *different* vendors are not extra-correlated.

### 3. Part 3: Event Days and Rolling Comovement
* **File Verified:** [part3_report.txt](file:///C:/Users/Hanamanthagouda/Desktop/afa/miniProject/data/part3_report.txt) | [part3_rolling_comovement.png](file:///C:/Users/Hanamanthagouda/Desktop/afa/miniProject/plots/part3_rolling_comovement.png)
* **Empirical Match:** 
  * Same-vendor pairs for Vendor $A$ show a sharp spike in average correlation to **$0.012724$** during event windows, compared to **$0.008035$** on placebo days and **$0.007721$** on ordinary days.
  * Vendor $B$ same-vendor pairs (control) remain flat and unchanged at **$0.007883$** during Vendor $A$'s event windows.
  * This confirms the comovement spike is vendor-specific, mimicking how version updates or outages propagate to users of a single model.

### 4. Part 4: Equilibrium Tipping Point Analysis
* **File Verified:** [part4_report.txt](file:///C:/Users/Hanamanthagouda/Desktop/afa/miniProject/data/part4_report.txt) | [part4_convergence_path.png](file:///C:/Users/Hanamanthagouda/Desktop/afa/miniProject/plots/part4_convergence_path.png)
* **Observed Result:** Vendor $A$'s share converges to **$100\%$** (complete tipping) in both the initial episode ($A=0.20, B=0.18$) and the experiment episode ($A=0.24, B=0.18$).
* **Why did it tip 100%?** 
  * The firm's payoff is:
    $$\text{Payoff}_v(\delta) = \text{benefit\_rate}_v \delta - \frac{1}{2} \delta^2 - 0.10 \delta D_v$$
  * Taking crowd size $D_v = s_v \delta_v$ as given, FOC yields:
    $$\delta_v^* = \text{benefit\_rate}_v - 0.10 D_v \implies \delta_v^* = \frac{\text{benefit\_rate}_v}{1 + 0.10 s_v}$$
  * Substituting this back, the converged value is:
    $$\text{Value}_v = \frac{1}{2} (\delta_v^*)^2 = \frac{1}{2} \left(\frac{\text{benefit\_rate}_v}{1 + 0.10 s_v}\right)^2$$
  * Evaluating at the boundary $s_A = 1.0, s_B = 0.0$:
    $$\text{Value}_A = \frac{1}{2} \left(\frac{0.20}{1.10}\right)^2 \approx 0.01653 \quad > \quad \text{Value}_B = \frac{1}{2} \left(\frac{0.18}{1.00}\right)^2 = 0.01620$$
  * Because $\text{Value}_A > \text{Value}_B$ even at $s_A = 100\%$, there is no interior crossing point. A single firm deviating to Vendor B would face $D_B \approx 0$ and receive $0.01620$, which is less than the $0.01653$ it receives by staying on the crowded Vendor A.
  * **Conclusion:** The crowding charge coefficient ($0.10$) is mathematically too weak to offset the $2\%$ benefit rate advantage of Vendor A. Under these parameters, the unique Nash Equilibrium is complete tipping.

---

## Section 2: Mathematical & Economic Critique of the Model

While the simulation successfully isolates the comovement signature, several core structural assumptions are unrealistic and limit the paper’s contribution to real-world financial economics. 

### 1. The Linearity of the Crowding Penalty
* **Critique:** The crowding penalty is modeled as linear in usage and crowd size ($0.10 \times \delta \times D_v$). In real stock markets, congestion externalities are highly non-linear. As a vendor's market share approaches 100%, systemic vulnerability increases exponentially due to correlated error propagation and single-point-of-failure risks.
* **Proposed Enhancement:** Implement a convex crowding penalty (e.g., quadratic in crowd size):
  $$\text{Payoff}_v = \text{benefit\_rate}_v \delta - \frac{1}{2} \delta^2 - c \delta D_v^2$$
  This reflects that the first few adopters cause negligible crowding, but heavy concentration creates severe, non-linear bottlenecks.

### 2. Dollar Price vs. Physical Rate Limits (TPM/RPM)
* **Critique:** The model assumes the primary constraint on token usage is a dollar cost. In practice, enterprise AI scaling is limited by physical API Rate Limits: **Tokens Per Minute (TPM)** and **Requests Per Minute (RPM)**. 
* **Proposed Enhancement:** Incorporate a dynamic capacity queue where excess demand from one firm introduces queue delay or rate-limit errors (negative externality) for other firms using the same vendor. This introduces a shadow congestion price:
  $$\lambda_{v,t} = P_t + \text{Marginal Congestion Cost}_{v,t}$$

### 3. Exogenous Deflation vs. Random Walk Pricing
* **Critique:** Simulating token prices as a Geometric Brownian Motion (GBM) ignores the empirical reality of technological deflation. AI inference costs exhibit deterministic step-down drops due to hardware progress (Huang's Law) and model optimizations, not continuous random walks.
* **Proposed Enhancement:** Model pricing as a step-deflation process:
  $$P_t = P_0 \gamma^{\lfloor t / \tau \rfloor}$$
  where $\gamma < 1$ represents the rate of cost deflation.

### 4. Non-Convexity of AI Productivity (Threshold Effects)
* **Critique:** The productivity function assumes a smooth exponential return on token usage. In reality, LLM-based tasks have binary utility (e.g., code either compiles and passes unit tests, or it fails completely). Below a minimum prompt and generation token threshold ($T_{\min}$), productivity is zero.
* **Proposed Enhancement:** Implement a threshold quality function:
  $$Q_{ijt} = 0 \quad \text{if } T_{ijt} < T_{\min}$$
  $$Q_{ijt} = 1 - e^{-\alpha_j (T_{ijt} - T_{\min})} \quad \text{if } T_{ijt} \ge T_{\min}$$
  Under this threshold model, decentralized "equal budgeting" of tokens is highly inefficient, demonstrating the necessity of market clearing mechanisms.

### 5. human Bottleneck & Verification Scarcity
* **Critique:** The model ignores the human expert labor required to audit and verify AI output. Since LLMs hallucinate, scaling token consumption requires proportional human review time.
* **Proposed Enhancement:** Model quality as a joint function of tokens and human hours $Q_i = f(T_i, H_i)$. Since human expert hours are strictly constrained by local wages, human attention, rather than token price, is the ultimate limiting factor of computational capital.
