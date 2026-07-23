# Research Executive Memo: Re-Solving the Equilibrium & Exact Decomposition (Parts 9–12)

## 1. Executive Summary

This memorandum synthesizes the theoretical refinements, exact closed-form solutions, risk factorizations, and survival region mapping across **Parts 9 through 12** (Round 3) of the research project *"Computational Capital Budgeting: Simulation Design for Allocating Scarce AI Tokens."*

In Round 3, theoretical refinements yielded exact closed-form formulas for all equilibrium quantities. The previous coarse $5\%$-reallocation discretization has been replaced by exact mathematical solutions and verified against a continuous bisection iterative solver to machine precision.

---

## 2. Deliverables & Key Findings (Parts 9–12)

### Part 9: Exact Equilibrium Solver & Certification (Table 1)
- **Problem & Refinement:** The previous $5\%$-step grid discretized market shares into coarse multiples of $5\%$. The exact equilibrium solver now calculates continuous closed-form solutions:
  $$\bar{m} = \frac{\Delta_a + \Delta_b}{2 + k/\chi}, \quad D_a = \frac{\Delta_a - \bar{m}}{k}, \quad D_b = \frac{\Delta_b - \bar{m}}{k}$$
- **Verification:** Comparison of the exact closed-form formula against a continuous bisection solver across Interior ($\Delta_a=0.190, \Delta_b=0.180$), Boundary ($\Delta_a=0.198, \Delta_b=0.180$), and Tipped ($\Delta_a=0.216, \Delta_b=0.180$) regimes yields **exact agreement to at least 12 decimal places** (max discrepancy $< 10^{-12}$).

### Part 10: Smooth Quality Ratio Sweep & Corrected Frontier Experiment (Table 2, Figures 1 & 2)
- **Quality Ratio Sweep:** Holding $\Delta_b = 0.18$ and varying the quality ratio $R = \Delta_a / \Delta_b$ from $1.00$ to $1.28$:
  - Leader market share $s_a$ rises smoothly from $50.0\%$ at parity ($R = 1.00$) to $95.0\%$ just below the tipping threshold ($R = 1.0999$), then jumps discontinuously to $100.0\%$ at $R = 1.10$. No discrete staircase artifact remains.
  - Total systematic risk rises continuously throughout the interior region, nearly doubling prior to market tipping.
- **Corrected Frontier Experiment ($\Delta_a = 0.190 \to 0.195, \Delta_b = 0.180$):**
  - **Leader Market Share:** Moves cleanly from **$78.38\%$ to $92.00\%$** (an absolute increase of $+13.62$ percentage points, or $+17.38\%$ relative increase).
  - **Total Systematic Risk:** Surges by **$+32.51\%$** (from $0.004104$ to $0.005439$).
  - **Decomposition of Risk Change:** Of the total $+32.51\%$ risk surge:
    - **$+2.72$ percentage points** stem from higher overall AI adoption ($\delta^{\text{tot}}$ growing $+1.35\%$).
    - **$+29.00$ percentage points** stem from higher market concentration ($\text{HHI}$ jumping from $0.6611$ to $0.8528$).

### Part 11: Exact Systematic Risk Factorization Verification
- **Theory:** Systematic risk factors exactly into an adoption component and a concentration component:
  $$\text{Systematic Risk} = \underbrace{0.2 \times (\delta^{\text{tot}})^2}_{\text{Adoption}} \times \underbrace{\text{HHI}}_{\text{Concentration}}$$
- **Result:** Across all 200 points of the quality ratio sweep ($R \in [1.00, 1.28]$), the maximum absolute discrepancy between the factored product and direct systematic risk is **$0.00 \times 10^{0}$** (exact identity to machine floating-point precision).

### Part 12: Dual Vendor Survival Region & Economic Interpretation (Table 3, Figure 3)
- **Survival Condition:** Dual vendors survive if and only if the quality ratio $R < 1 + k/\chi$, where $k = \gamma \theta \sigma_A^2 = 0.5 \theta$.
- **Survival Mapping ($\theta \in [0.01, 0.40], \chi \in [0.5, 4.0]$):**
  - Tipping thresholds range from **$1.006$** (weakly correlated errors $\theta = 0.05$, expensive integration $\chi = 4.0$) to **$1.400$** (strongly correlated errors $\theta = 0.40$, cheap integration $\chi = 0.5$).
  - At our calibration point ($\theta = 0.20, \chi = 1.00$), the threshold is exactly **$1.100$**.
- **Economic Insight:** Market diversity is most fragile where AI vendor errors are least correlated ($\theta \to 0$), because uncorrelated errors offer maximal risk diversification benefit, driving aggressive firm concentration into the lead vendor. Conversely, vendor diversity is most robust where AI errors are highly correlated ($\theta \to 0.40$).

---

## 3. Summary Table of Round 3 Deliverables & Target Values

| Part | Deliverable / Quantity | Exact Target / Output | Economic Meaning / Verdict |
| :--- | :--- | :--- | :--- |
| **Part 9** | Formula vs Solver Table | Max diff $< 10^{-12}$ | Certifies exact closed-form solution |
| **Part 10**| Frontier Leader Share | **$78.38\% \to 92.00\%$** | Corrects coarse 80% rounding artifact |
| **Part 10**| Systematic Risk Surge | **$+32.51\%$** | +2.7% adoption, +29.0% concentration |
| **Part 11**| Risk Identity Check | Max diff $= 0.00$ | Identity verified to machine precision |
| **Part 12**| Calibration Threshold | **$1.1000$** ($\theta=0.20, \chi=1.00$) | Boundary between interior & tipping |
| **Part 12**| Survival Region Range | **$1.0063 \dots 1.4000$** | Diversity fragile when errors uncorrelated |

---

*Memo compiled for Round 3 in [memo_9to12.md](file:///C:/Users/Hanamanthagouda/Desktop/afa/miniProject/memo_9to12.md).*
