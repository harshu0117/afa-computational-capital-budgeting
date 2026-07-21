# [Human-Authored]
# Parameters for Monte Carlo simulation
MC_FIRMS = 300
MC_PAIRS = 5000
MC_SEEDS = range(1, 201) # 200 replications
THETA_GRID = [0.0, 0.05, 0.10, 0.20]

# [AI-Generated]
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

# Add current directory to path to ensure simulation_core is importable
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from run_part2 import calculate_residuals
from run_part5 import compute_ols_and_clustered_se, compute_dyadic_clustered_se

def run_single_mc_replication(seed, theta, num_firms=MC_FIRMS, num_pairs=MC_PAIRS, num_days=1000):
    """
    Runs a single simulation replication for a given seed and theta value.
    """
    np.random.seed(seed)
    
    # 1. Firm assignments (60% vendor A, 40% vendor B)
    vendor_a_count = int(num_firms * 0.6)
    vendors = np.array(['A'] * vendor_a_count + ['B'] * (num_firms - vendor_a_count))
    delta = np.random.uniform(0.0, 0.4, size=num_firms)
    beta = np.random.normal(1.0, 0.3, size=num_firms)
    
    # 2. Daily shocks
    m = np.random.normal(0.0, 1.0, size=num_days)
    eta_A = np.random.normal(0.0, 1.0, size=num_days)
    eta_B = np.random.normal(0.0, 1.0, size=num_days)
    epsilon = np.random.normal(0.0, 1.0, size=(num_days, num_firms))
    
    eta_v = np.zeros((num_days, num_firms))
    eta_v[:, :vendor_a_count] = eta_A[:, np.newaxis]
    eta_v[:, vendor_a_count:] = eta_B[:, np.newaxis]
    
    # 3. Build returns
    market_part = np.outer(m, beta)
    shared_ai_part = delta * np.sqrt(theta) * eta_v
    firm_luck = np.sqrt(1.0 - (delta**2) * theta) * epsilon
    r = market_part + shared_ai_part + firm_luck
    
    # 4. Residuals
    residuals = calculate_residuals(r, m)
    corr_matrix = np.corrcoef(residuals, rowvar=False)
    
    # 5. Pair sampling
    pairs = []
    while len(pairs) < num_pairs:
        i_idx = np.random.randint(0, num_firms, size=num_pairs - len(pairs))
        j_idx = np.random.randint(0, num_firms, size=num_pairs - len(pairs))
        mask = i_idx != j_idx
        valid = np.column_stack([i_idx[mask], j_idx[mask]])
        pairs.extend(valid.tolist())
    pairs = np.array(pairs[:num_pairs])
    
    # Features
    corr_vals = np.array([corr_matrix[i, j] for i, j in pairs])
    same_vendor = np.array([vendors[i] == vendors[j] for i, j in pairs], dtype=float)
    delta_prod = np.array([delta[i] * delta[j] for i, j in pairs])
    
    X = np.column_stack([np.ones(len(pairs)), same_vendor, same_vendor * delta_prod, delta_prod])
    
    # OLS and Clustered SE
    beta_est, res_vec, XTX_inv, _ = compute_ols_and_clustered_se(X, corr_vals)
    se_cluster = compute_dyadic_clustered_se(X, res_vec, XTX_inv, pairs)
    t_stats = beta_est / se_cluster
    
    # Correlation gap (same vendor minus cross vendor)
    corr_gap = np.mean(corr_vals[same_vendor == 1.0]) - np.mean(corr_vals[same_vendor == 0.0])
    
    return beta_est, t_stats, corr_gap

def run_part6():
    print("=== PART 6: Replace Luck with Distributions (Monte Carlo Replications) ===")
    print(f"Running 200 replications over theta grid {THETA_GRID} using N={MC_FIRMS} firms and {MC_PAIRS} pairs...")
    
    results_by_theta = {}
    
    for theta in THETA_GRID:
        print(f"\nProcessing theta = {theta}...")
        betas_list = []
        tstats_list = []
        gaps_list = []
        
        for s in MC_SEEDS:
            b_est, t_stat, gap = run_single_mc_replication(seed=s, theta=theta)
            betas_list.append(b_est)
            tstats_list.append(t_stat)
            gaps_list.append(gap)
            
        betas_arr = np.array(betas_list)   # shape (200, 4)
        tstats_arr = np.array(tstats_list) # shape (200, 4)
        
        # Power of b2 test (fraction of runs where |t_b2| >= 1.96)
        power_b2 = np.mean(np.abs(tstats_arr[:, 2]) >= 1.96)
        
        # False positive rate at theta = 0 (fraction where any b1, b2, or b3 is significant at 5%)
        any_sig = np.mean(np.any(np.abs(tstats_arr[:, 1:]) >= 1.96, axis=1))
        
        results_by_theta[theta] = {
            'mean_beta': np.mean(betas_arr, axis=0),
            'std_beta': np.std(betas_arr, axis=0),
            'power_b2': power_b2,
            'any_sig': any_sig,
            'mean_gap': np.mean(gaps_list)
        }
        
    # Print Table
    print("\nTable 7: Monte Carlo Results (Means and Standard Deviations Across 200 Runs)")
    print("=" * 85)
    print(f"{'Theta':<8} | {'b1 Mean (SD)':<18} | {'b2 Mean (SD)':<20} | {'b3 Mean (SD)':<18} | {'b2 Power':<10}")
    print("=" * 85)
    for theta in THETA_GRID:
        res = results_by_theta[theta]
        b1_str = f"{res['mean_beta'][1]:.4f} ({res['std_beta'][1]:.4f})"
        b2_str = f"{res['mean_beta'][2]:.4f} ({res['std_beta'][2]:.4f})"
        b3_str = f"{res['mean_beta'][3]:.4f} ({res['std_beta'][3]:.4f})"
        print(f"{theta:<8.2f} | {b1_str:<18} | {b2_str:<20} | {b3_str:<18} | {res['power_b2']*100:>9.1f}%")
    print("=" * 85)
    print(f"False Positive Rate at theta = 0.0: {results_by_theta[0.0]['any_sig']*100:.1f}%")
    print("=" * 85)
    
    # Plot Power Curve
    powers = [results_by_theta[t]['power_b2'] * 100 for t in THETA_GRID]
    plt.figure(figsize=(8, 5))
    plt.plot(THETA_GRID, powers, 'o-', color='darkblue', linewidth=2, label='Statistical Power of b2 Test')
    plt.axhline(y=5.0, color='red', linestyle='--', label='5% Significance Level (False Positive Threshold)')
    plt.xlabel('True Vendor Shock Intensity ($\\theta$)')
    plt.ylabel('Rejection Rate / Power (%)')
    plt.title('Monte Carlo Power Curve for Shared AI Vendor Effect (b2 Test)')
    plt.ylim(0, 105)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    
    os.makedirs('plots', exist_ok=True)
    plt.savefig('plots/part6_power_curve.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved Monte Carlo power curve figure to plots/part6_power_curve.png")
    
    # Save Report
    with open('data/part6_report.txt', 'w') as f:
        f.write("Table 7: Monte Carlo Results Across 200 Replications\n")
        f.write("=" * 85 + "\n")
        f.write(f"{'Theta':<8} | {'b1 Mean (SD)':<18} | {'b2 Mean (SD)':<20} | {'b3 Mean (SD)':<18} | {'b2 Power':<10}\n")
        f.write("=" * 85 + "\n")
        for theta in THETA_GRID:
            res = results_by_theta[theta]
            b1_str = f"{res['mean_beta'][1]:.4f} ({res['std_beta'][1]:.4f})"
            b2_str = f"{res['mean_beta'][2]:.4f} ({res['std_beta'][2]:.4f})"
            b3_str = f"{res['mean_beta'][3]:.4f} ({res['std_beta'][3]:.4f})"
            f.write(f"{theta:<8.2f} | {b1_str:<18} | {b2_str:<20} | {b3_str:<18} | {res['power_b2']*100:>9.1f}%\n")
        f.write("=" * 85 + "\n")
        f.write(f"False Positive Rate at theta = 0.0: {results_by_theta[0.0]['any_sig']*100:.1f}%\n")

if __name__ == "__main__":
    run_part6()
