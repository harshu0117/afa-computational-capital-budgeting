# [Human-Authored]
# Parameters for diagnostic ladder
DIAG_SEED = 42
TRUE_THETA = 0.20

# [AI-Generated]
import numpy as np
import os
import sys

# Add current directory to path to ensure simulation_core is importable
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from simulation_core import generate_market_data, NUM_FIRMS, NUM_DAYS
from run_part2 import calculate_residuals
from run_part5 import compute_ols_and_clustered_se

def run_part7():
    print("=== PART 7: Explain the Missing 18% (Diagnostic Ladder) ===")
    
    # Generate baseline data for Dataset ONE (seed 42, T=1000)
    data = generate_market_data(TRUE_THETA)
    r = data['r']
    m = data['m']
    beta_true = data['beta']
    delta = data['delta']
    vendors = data['vendors']
    
    # Sample 20,000 pairs (seed 42)
    np.random.seed(42)
    pairs = []
    while len(pairs) < 20000:
        i_idx = np.random.randint(0, NUM_FIRMS, size=20000 - len(pairs))
        j_idx = np.random.randint(0, NUM_FIRMS, size=20000 - len(pairs))
        mask = i_idx != j_idx
        valid = np.column_stack([i_idx[mask], j_idx[mask]])
        pairs.extend(valid.tolist())
    pairs = np.array(pairs[:20000])
    
    same_vendor = np.array([vendors[i] == vendors[j] for i, j in pairs], dtype=float)
    delta_prod = np.array([delta[i] * delta[j] for i, j in pairs])
    X_full = np.column_stack([np.ones(len(pairs)), same_vendor, same_vendor * delta_prod, delta_prod])
    
    # Baseline Round 1 estimation
    res_est = calculate_residuals(r, m)
    corr_est = np.corrcoef(res_est, rowvar=False)
    Y_base = np.array([corr_est[i, j] for i, j in pairs])
    beta_base, _, _, se_base = compute_ols_and_clustered_se(X_full, Y_base)
    b2_base = beta_base[2]
    
    # Rung 1: Oracle Residuals (using true beta_i)
    # Oracle residuals: u_it = r_it - beta_i * m_t
    market_part = np.outer(m, beta_true)
    res_oracle = r - market_part
    corr_oracle = np.corrcoef(res_oracle, rowvar=False)
    Y_oracle = np.array([corr_oracle[i, j] for i, j in pairs])
    beta_oracle, _, _, se_oracle = compute_ols_and_clustered_se(X_full, Y_oracle)
    b2_oracle = beta_oracle[2]
    
    # Rung 2: Fisher Transformation (z = 0.5 * ln((1+r)/(1-r)))
    # Apply Fisher z-transform to estimated residual correlations
    z_vals = 0.5 * np.log((1.0 + Y_base) / (1.0 - Y_base))
    beta_fisher, _, _, se_fisher = compute_ols_and_clustered_se(X_full, z_vals)
    b2_fisher = beta_fisher[2]
    
    # Rung 3: Large Sample Length (T = 4,000 days)
    # Generate market data directly for num_days=4000 without PRNG re-seeding overlap
    print("Generating T=4,000 dataset for Rung 3 directly via simulation_core...")
    data_4k = generate_market_data(TRUE_THETA, num_days=4000)
    res_4k = calculate_residuals(data_4k['r'], data_4k['m'])
    corr_4k = np.corrcoef(res_4k, rowvar=False)
    Y_4k = np.array([corr_4k[i, j] for i, j in pairs])
    beta_4k, _, _, se_4k = compute_ols_and_clustered_se(X_full, Y_4k)
    b2_4k = beta_4k[2]
    
    # Rung 4: Specification (Same-vendor pairs only: rho_ij = a + theta * delta_i * delta_j)
    same_vendor_mask = (same_vendor == 1.0)
    Y_same = Y_base[same_vendor_mask]
    X_same = np.column_stack([np.ones(np.sum(same_vendor_mask)), delta_prod[same_vendor_mask]])
    beta_spec, _, _, se_spec = compute_ols_and_clustered_se(X_same, Y_same)
    b2_spec = beta_spec[1] # slope coefficient
    
    # Print Table
    print("\nTable 8: Diagnostic Ladder for the Usage Slope (Target: True Theta = 0.200)")
    print("=" * 80)
    print(f"{'Rung / Model Specification':<45} | {'Estimated Slope':<18} | {'Gap from 0.200':<15}")
    print("=" * 80)
    print(f"{'0. True Theoretical Value':<45} | {TRUE_THETA:>18.4f} | {0.0:>15.4f}")
    print(f"{'1. Round 1 Baseline (Estimated beta, T=1000)':<45} | {b2_base:>18.4f} | {TRUE_THETA - b2_base:>15.4f}")
    print(f"{'2. Oracle Residuals (True beta_i used)':<45} | {b2_oracle:>18.4f} | {TRUE_THETA - b2_oracle:>15.4f}")
    print(f"{'3. Fisher z-Transformation':<45} | {b2_fisher:>18.4f} | {TRUE_THETA - b2_fisher:>15.4f}")
    print(f"{'4. Large Sample Length (T=4,000 days)':<45} | {b2_4k:>18.4f} | {TRUE_THETA - b2_4k:>15.4f}")
    print(f"{'5. Same-Vendor Specification Only':<45} | {b2_spec:>18.4f} | {TRUE_THETA - b2_spec:>15.4f}")
    print("=" * 80)
    
    # Save Report
    os.makedirs('data', exist_ok=True)
    with open('data/part7_report.txt', 'w') as f:
        f.write("Table 8: Diagnostic Ladder for the Usage Slope\n")
        f.write("=" * 80 + "\n")
        f.write(f"{'Rung / Model Specification':<45} | {'Estimated Slope':<18} | {'Gap from 0.200':<15}\n")
        f.write("=" * 80 + "\n")
        f.write(f"{'0. True Theoretical Value':<45} | {TRUE_THETA:>18.4f} | {0.0:>15.4f}\n")
        f.write(f"{'1. Round 1 Baseline (Estimated beta, T=1000)':<45} | {b2_base:>18.4f} | {TRUE_THETA - b2_base:>15.4f}\n")
        f.write(f"{'2. Oracle Residuals (True beta_i used)':<45} | {b2_oracle:>18.4f} | {TRUE_THETA - b2_oracle:>15.4f}\n")
        f.write(f"{'3. Fisher z-Transformation':<45} | {b2_fisher:>18.4f} | {TRUE_THETA - b2_fisher:>15.4f}\n")
        f.write(f"{'4. Large Sample Length (T=4,000 days)':<45} | {b2_4k:>18.4f} | {TRUE_THETA - b2_4k:>15.4f}\n")
        f.write(f"{'5. Same-Vendor Specification Only':<45} | {b2_spec:>18.4f} | {TRUE_THETA - b2_spec:>15.4f}\n")
        f.write("=" * 80 + "\n")

if __name__ == "__main__":
    run_part7()
