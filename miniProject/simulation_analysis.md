# Shared-AI-Vendor Effect: Comprehensive Simulation Report & Economic Critique (Rounds 1 & 2)

**Document Version:** 3.0  
**Target Submission:** American Finance Association (AFA) Special Session  
**Code Workspace:** [miniProject](file:///C:/Users/Hanamanthagouda/Desktop/afa/miniProject)  
**Primary Specifications:** [AFA_Simulation_V1.pdf](file:///C:/Users/Hanamanthagouda/Desktop/afa/miniProject/AFA_Simulation_V1.pdf) | [AFA_Simulation_V2.pdf](file:///C:/Users/Hanamanthagouda/Desktop/afa/miniProject/AFA_Simulation_V2.pdf)

---

## Executive Summary

This document provides a complete summary of the simulation deliverables and a rigorous mathematical and economic critique across all eight project parts (Rounds 1 and 2).

---

## Part I: Empirical Deliverables & Output Summary

### 1. Round 1 Deliverables (Parts 1–4)
* **Part 1 (Fake Market Setup):** $N = 500$ firms, $T = 1,000$ days. Vendor $A$ share = $60\%$ ($300$ firms), Vendor $B$ share = $40\%$ ($200$ firms). Firm usages $\delta_i \sim U[0, 0.4]$, market sensitivities $\beta_i \sim N(1, 0.3^2)$. Generated identical firm assignments across `Dataset ONE` ($\theta = 0.2$) and `Dataset ZERO` ($\theta = 0.0$).
* **Part 2 (Detection Machinery):** Residual returns computed per firm via OLS regression $r_{it} = \hat{\alpha}_i + \hat{\beta}_i m_t + u_{it}$. In `Dataset ONE`, same-vendor pair correlations average $0.0081$ (cross-vendor $-0.0001$) with $b_2 > 0$ highly significant ($t \approx 11.85$). In `Dataset ZERO`, all correlations and coefficients vanish toward zero.
* **Part 3 (Event Days):** Vendor $A$'s shock variance scaled to $5^2$ on 10 event days. Rolling 11-day comovement spikes sharply for Vendor $A$ pairs during event windows ($0.0127$) while remaining flat for Vendor $B$ control pairs ($0.0079$).
* **Part 4 (Market Tipping Baseline):** Under initial parameters ($A=0.20, B=0.18$), Vendor $A$'s quality advantage ($0.02$) exceeds the linear crowding charge capacity ($\approx 0.018$), causing $100\%$ market tipping to Vendor $A$.

### 2. Round 2 Deliverables (Parts 5–8)
* **Part 5 (Three-Way Standard Errors):** Evaluated Plain OLS, Dyadic Two-Way Clustered by firm, and 1,000-draw Firm-Level Bootstrap standard errors across both datasets. Dyadic clustering inflates standard errors by $2\text{--}4\times$, eliminating spurious null significance under `Dataset ZERO`.
* **Part 6 (Monte Carlo Distributions):** Executed 200 simulation replications across seeds $1, \dots, 200$ for $\theta \in \{0.0, 0.05, 0.10, 0.20\}$ ($N=300, 5,000$ pairs). Generated the statistical power curve ($b_2$ power near $100\%$ at $\theta=0.20$) and verified false-positive rates at $\theta=0.0$ ($5\%$).
* **Part 7 (Diagnostic Ladder):** Diagnosed the $18\%$ usage slope shortfall ($0.165$ vs. $0.200$) across oracle residuals (true $\beta_i$), Fisher $z$-transformations, large sample length ($T=4,000$), and same-vendor-only specifications.
* **Part 8 (Tipping Boundary & Interior Frontier):** Executed a 21-run quality gap sweep ($0.000$ to $0.050$), overlaid the theoretical tipping kink at gap $\approx 0.018$, plotted market-wide systematic risk $0.2(D_A^2 + D_B^2)$, and completed the interior frontier experiment ($0.190 \rightarrow 0.195$).

---

## Part II: Constructive Critique of Round 1 Architecture (V1)

1. **Linearity of Crowding Penalty:** The linear crowding charge ($0.10 \delta D_v$) fails to prevent complete market tipping when benefit gaps exceed $0.018$. Real market congestion is non-linear.
2. **Dollar Cost vs. Physical Rate Limits (TPM/RPM):** Real enterprise AI scaling is constrained by API Rate Limits (Tokens Per Minute), creating shadow congestion prices omitted in simple market models.
3. **Deterministic Deflation vs. Random Walk Pricing:** Token prices follow technological step-down deflation (Huang's Law) rather than continuous random walks.
4. **Non-Convexity of AI Productivity:** Code generation and automated reasoning exhibit step-like non-convexities (binary pass/fail unit tests), making smooth exponential productivity functions unrealistic.
5. **Human Verification Bottlenecks:** LLM outputs require scarce human expert verification time, making human attention the ultimate scaling bottleneck.

---

## Part III: Constructive Critique of Round 2 Architecture (V2)

### 1. Inference & Dyadic Clustering Limitations (Part 5)
* **Mathematical Assessment:** Dyadic clustering (Cameron, Gelbach, & Miller 2011) corrects for cross-sectional firm pair overlap ($i_k = i_m$ or $j_k = j_m$) but assumes independence across trading days $t$. In real financial markets, asset returns exhibit **temporal clustering** (GARCH volatility clustering and autocorrelated market/vendor shocks).
* **Economic Shortcoming:** Vendor outages and model updates exhibit temporal persistence. Dyadic clustering understates standard errors when vendor shocks display autocorrelation over time.
* **Proposed Enhancement:** Implement multi-way clustering over (Firm $i$, Firm $j$, Time $t$) or time-block bootstrapping to preserve temporal dependence.

### 2. Monte Carlo Power & Gaussian Normality Assumptions (Part 6)
* **Mathematical Assessment:** The Monte Carlo power sweep assumes thin-tailed Gaussian normal distributions ($\eta_{v,t} \sim N(0, 1)$). Real asset returns and AI vendor shocks display heavy tails (excess kurtosis) and jump dynamics.
* **Economic Shortcoming:** LLM failures (e.g., widespread hallucinations, security vulnerabilities) follow power-law distributions. Assuming normality overstates finite-sample statistical power and underpredicts tail risk.
* **Proposed Enhancement:** Re-evaluate Monte Carlo power curves under fat-tailed Student-$t$ error distributions ($df \in [3, 5]$) and jump-diffusion shock processes.

### 3. Endogenous Usage & Attenuation Bias in Diagnostic Ladder (Part 7)
* **Mathematical Assessment:** The diagnostic ladder attributes the $18\%$ slope shortfall ($0.165$ vs. $0.200$) to sample noise, $\hat{\beta}_i$ estimation error, and specification collinearity, while treating firm usage $\delta_i$ as statically fixed and exogenous.
* **Economic Shortcoming:** Firms dynamically adjust their AI usage $\delta_{i,t}$ based on model quality, pricing, and observed vendor performance. Treating $\delta_i$ as static creates classical errors-in-variables (attenuation bias) that simple linear ladders cannot eliminate.
* **Proposed Enhancement:** Formulate an Instrumental Variables (IV) specification using exogenous vendor outage events as instruments, or model dynamic usage $\delta_{i,t}$ to estimate the unattenuated usage slope.

### 4. Linear Crowding Charges & Abrupt Tipping Kinks (Part 8)
* **Mathematical Assessment:** The theoretical tipping boundary exhibits a sharp, piecewise-linear "kink" at gap $\approx 0.10 \times \delta^* \approx 0.018$, where market share jumps linearly until $100\%$ tipping.
* **Economic Shortcoming:** Real enterprise markets rarely exhibit sharp deterministic kinks. Switching costs ($S > 0$), multi-homing (using both vendors simultaneously), and non-linear capacity bottlenecks create smooth adoption S-curves rather than abrupt linear tipping.
* **Proposed Enhancement:** Incorporate firm switching costs $S > 0$ and a quadratic crowding penalty ($c \delta D_v^2$) to transform the rigid theoretical kink into a smooth, stochastic market equilibrium.
