# [Human-Authored]
# Parameters loaded from simulation_core.py
N_BOOTSTRAP = 1000
SEED_BOOTSTRAP = 42

# [AI-Generated]
import numpy as np
import os
import sys

# Add current directory to path to ensure simulation_core is importable
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from simulation_core import generate_market_data, THETA_ONE, THETA_ZERO, NUM_FIRMS
from run_part2 import calculate_residuals

def compute_ols_and_clustered_se(X, Y):
    """
    Computes OLS coefficients, plain OLS standard errors, 
    and dyadic firm-level two-way clustered standard errors.
    X: shape (M, K) design matrix
    Y: shape (M,) outcome vector
    """
    M, K = X.shape
    XTX_inv = np.linalg.inv(X.T @ X)
    beta = XTX_inv @ (X.T @ Y)
    residuals = Y - (X @ beta)
    
    # 1. Plain OLS Standard Errors
    sigma_sq = (residuals.T @ residuals) / (M - K)
    vcov_ols = sigma_sq * XTX_inv
    se_plain = np.sqrt(np.diag(vcov_ols))
    
    return beta, residuals, XTX_inv, se_plain

def compute_dyadic_clustered_se(X, residuals, XTX_inv, pairs):
    """
    Computes two-way dyadic clustered standard errors by firm.
    pairs: shape (M, 2) giving (firm_i, firm_j) for each pair
    """
    M, K = X.shape
    Xe = X * residuals[:, np.newaxis] # shape (M, K)
    
    # Accumulate score vectors per firm
    u_firm = np.zeros((NUM_FIRMS, K))
    for k in range(M):
        i, j = pairs[k]
        u_firm[i] += Xe[k]
        u_firm[j] += Xe[k]
        
    # Dyadic sandwich matrix
    M_cluster = u_firm.T @ u_firm
    vcov_cluster = XTX_inv @ M_cluster @ XTX_inv
    se_clustered = np.sqrt(np.diag(vcov_cluster))
    
    return se_clustered

def run_firm_bootstrap(residuals_mat, delta, vendors, pairs_orig, n_bootstrap=1000):
    """
    Runs firm-level bootstrap (re-sampling firms, rebuilding pairs without diagonal self-pairs).
    """
    np.random.seed(SEED_BOOTSTRAP)
    boot_betas = []
    num_pairs = len(pairs_orig)
    
    for b in range(n_bootstrap):
        # 1. Re-sample firms with replacement
        sampled_firms = np.random.choice(NUM_FIRMS, size=NUM_FIRMS, replace=True)
        
        # 2. Re-sample pairs from sampled_firms filtering out self-pairs (idx_i != idx_j)
        pairs_boot = []
        while len(pairs_boot) < num_pairs:
            idx_i_cand = np.random.choice(sampled_firms, size=num_pairs - len(pairs_boot))
            idx_j_cand = np.random.choice(sampled_firms, size=num_pairs - len(pairs_boot))
            mask = idx_i_cand != idx_j_cand
            valid = np.column_stack([idx_i_cand[mask], idx_j_cand[mask]])
            pairs_boot.extend(valid.tolist())
        pairs_boot = np.array(pairs_boot[:num_pairs])
        
        idx_i = pairs_boot[:, 0]
        idx_j = pairs_boot[:, 1]
        
        # Calculate correlation matrix of residuals for fast lookup
        corr_matrix = np.corrcoef(residuals_mat, rowvar=False)
        
        # Extract features for bootstrap pairs
        corr_vals = corr_matrix[idx_i, idx_j]
        same_vendor = (vendors[idx_i] == vendors[idx_j]).astype(float)
        delta_prod = delta[idx_i] * delta[idx_j]
        
        X_boot = np.column_stack([np.ones(len(corr_vals)), same_vendor, same_vendor * delta_prod, delta_prod])
        
        # OLS estimation
        beta_boot = np.linalg.inv(X_boot.T @ X_boot) @ (X_boot.T @ corr_vals)
        boot_betas.append(beta_boot)
        
    boot_betas = np.array(boot_betas) # shape (n_bootstrap, K)
    se_bootstrap = np.std(boot_betas, axis=0)
    return se_bootstrap

def run_part5():
    print("=== PART 5: Fix the Inference (Three-Way Standard Errors) ===")
    
    # Generate datasets ONE and ZERO
    data_one = generate_market_data(THETA_ONE)
    data_zero = generate_market_data(THETA_ZERO)
    
    # Calculate residuals
    res_one = calculate_residuals(data_one['r'], data_one['m'])
    res_zero = calculate_residuals(data_zero['r'], data_zero['m'])
    
    # Draw pairs (seed 42)
    np.random.seed(42)
    pairs = []
    while len(pairs) < 20000:
        i_idx = np.random.randint(0, NUM_FIRMS, size=20000 - len(pairs))
        j_idx = np.random.randint(0, NUM_FIRMS, size=20000 - len(pairs))
        mask = i_idx != j_idx
        valid_pairs = np.column_stack([i_idx[mask], j_idx[mask]])
        pairs.extend(valid_pairs.tolist())
    pairs = np.array(pairs[:20000])
    
    # Compute pair features
    vendors = data_one['vendors']
    delta = data_one['delta']
    same_vendor = np.array([vendors[i] == vendors[j] for i, j in pairs], dtype=float)
    delta_prod = np.array([delta[i] * delta[j] for i, j in pairs])
    
    X = np.column_stack([np.ones(len(pairs)), same_vendor, same_vendor * delta_prod, delta_prod])
    
    # Correlation matrices
    corr_one = np.corrcoef(res_one, rowvar=False)
    corr_zero = np.corrcoef(res_zero, rowvar=False)
    
    Y_one = np.array([corr_one[i, j] for i, j in pairs])
    Y_zero = np.array([corr_zero[i, j] for i, j in pairs])
    
    # 1. Dataset ONE estimations
    beta_one, res_vec_one, XTX_inv_one, se_plain_one = compute_ols_and_clustered_se(X, Y_one)
    se_cluster_one = compute_dyadic_clustered_se(X, res_vec_one, XTX_inv_one, pairs)
    print("Running firm-level bootstrap for Dataset ONE (1,000 iterations)...")
    se_boot_one = run_firm_bootstrap(res_one, delta, vendors, pairs, n_bootstrap=N_BOOTSTRAP)
    
    # 2. Dataset ZERO estimations
    beta_zero, res_vec_zero, XTX_inv_zero, se_plain_zero = compute_ols_and_clustered_se(X, Y_zero)
    se_cluster_zero = compute_dyadic_clustered_se(X, res_vec_zero, XTX_inv_zero, pairs)
    print("Running firm-level bootstrap for Dataset ZERO (1,000 iterations)...")
    se_boot_zero = run_firm_bootstrap(res_zero, delta, vendors, pairs, n_bootstrap=N_BOOTSTRAP)
    
    # Print report table (All 3 SEs for both ONE and ZERO datasets)
    print("\nTable 6: Three-Way Standard Errors (Dataset ONE vs. Dataset ZERO)")
    print("=" * 115)
    print(f"{'Coefficient':<22} | {'Est (ONE)':<9} | {'Plain SE':<9} | {'Cluster SE':<10} | {'Boot SE':<9} | {'Est (ZERO)':<10} | {'Plain SE':<9} | {'Cluster SE':<10} | {'Boot SE':<9}")
    print("=" * 115)
    labels = ["b0 (Intercept)", "b1 (SameVendor)", "b2 (SameVendor x d_i d_j)", "b3 (d_i d_j)"]
    
    for k in range(4):
        print(f"{labels[k]:<22} | {beta_one[k]:>9.5f} | {se_plain_one[k]:>9.5f} | {se_cluster_one[k]:>10.5f} | {se_boot_one[k]:>9.5f} | {beta_zero[k]:>10.5f} | {se_plain_zero[k]:>9.5f} | {se_cluster_zero[k]:>10.5f} | {se_boot_zero[k]:>9.5f}")
    print("=" * 115)
    
    # Save report text
    os.makedirs('data', exist_ok=True)
    with open('data/part5_report.txt', 'w') as f:
        f.write("Table 6: Three-Way Standard Errors (Dataset ONE vs. Dataset ZERO)\n")
        f.write("=" * 115 + "\n")
        f.write(f"{'Coefficient':<22} | {'Est (ONE)':<9} | {'Plain SE':<9} | {'Cluster SE':<10} | {'Boot SE':<9} | {'Est (ZERO)':<10} | {'Plain SE':<9} | {'Cluster SE':<10} | {'Boot SE':<9}\n")
        f.write("=" * 115 + "\n")
        for k in range(4):
            f.write(f"{labels[k]:<22} | {beta_one[k]:>9.5f} | {se_plain_one[k]:>9.5f} | {se_cluster_one[k]:>10.5f} | {se_boot_one[k]:>9.5f} | {beta_zero[k]:>10.5f} | {se_plain_zero[k]:>9.5f} | {se_cluster_zero[k]:>10.5f} | {se_boot_zero[k]:>9.5f}\n")
        f.write("=" * 115 + "\n")

if __name__ == "__main__":
    run_part5()
