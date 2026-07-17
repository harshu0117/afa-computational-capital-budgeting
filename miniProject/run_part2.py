# [Human-Authored]
# No separate parameters required here (loaded from simulation_core.py)

# [AI-Generated]
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

# Add current directory to path to ensure simulation_core is importable
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from simulation_core import NUM_FIRMS, NUM_DAYS

def calculate_residuals(r, m):
    """
    Regresses each firm's return r_it on market factor m_t (with intercept)
    and returns the residuals.
    r: shape (NUM_DAYS, NUM_FIRMS)
    m: shape (NUM_DAYS,)
    Returns: shape (NUM_DAYS, NUM_FIRMS)
    """
    T = len(m)
    X = np.column_stack([np.ones(T), m]) # Design matrix with intercept
    # Vectorized OLS: beta = (X^T X)^-1 X^T r
    beta_hat = np.linalg.inv(X.T @ X) @ (X.T @ r)
    residuals = r - (X @ beta_hat)
    return residuals

def run_regression(corr_vals, same_vendor, delta_prod):
    """
    Runs the regression:
    corr_ij = b0 + b1*SameVendor_ij + b2*(SameVendor_ij * delta_i * delta_j) + b3*(delta_i * delta_j) + e_ij
    """
    n = len(corr_vals)
    # Define independent variables
    x0 = np.ones(n)
    x1 = same_vendor.astype(float)
    x2 = x1 * delta_prod
    x3 = delta_prod
    
    X = np.column_stack([x0, x1, x2, x3]) # shape (n, 4)
    Y = corr_vals
    
    # OLS coefficients
    XTX = X.T @ X
    beta = np.linalg.inv(XTX) @ (X.T @ Y)
    
    # Standard Errors
    residuals = Y - (X @ beta)
    sigma_sq = (residuals.T @ residuals) / (n - 4)
    vcov = sigma_sq * np.linalg.inv(XTX)
    se = np.sqrt(np.diag(vcov))
    
    return beta, se

def run_part2():
    print("=== PART 2: Verifying the Shared-AI-Vendor Effect ===")
    
    # Load data generated in Part 1
    if not os.path.exists('data/r_one.npy'):
        print("Error: Return data not found. Please run run_part1.py first.")
        return
        
    r_one = np.load('data/r_one.npy')
    r_zero = np.load('data/r_zero.npy')
    vendors = np.load('data/vendors.npy')
    delta = np.load('data/delta.npy')
    m = np.load('data/m.npy')
    
    # 1. Calculate residual returns
    residuals_one = calculate_residuals(r_one, m)
    residuals_zero = calculate_residuals(r_zero, m)
    
    # Save residuals for Part 3
    np.save('data/residuals_one.npy', residuals_one)
    
    # 2. Draw 20,000 random pairs of firms
    np.random.seed(SEED_PAIRS := 42)
    pairs = []
    while len(pairs) < 20000:
        i_idx = np.random.randint(0, NUM_FIRMS, size=20000 - len(pairs))
        j_idx = np.random.randint(0, NUM_FIRMS, size=20000 - len(pairs))
        mask = i_idx != j_idx
        valid_pairs = np.column_stack([i_idx[mask], j_idx[mask]])
        pairs.extend(valid_pairs.tolist())
    pairs = np.array(pairs[:20000])
    
    # Compute correlation matrix of residuals for both datasets
    corr_matrix_one = np.corrcoef(residuals_one, rowvar=False)
    corr_matrix_zero = np.corrcoef(residuals_zero, rowvar=False)
    
    # Record properties of each pair
    corr_vals_one = np.zeros(20000)
    corr_vals_zero = np.zeros(20000)
    same_vendor = np.zeros(20000, dtype=bool)
    delta_prod = np.zeros(20000)
    
    for idx, (i, j) in enumerate(pairs):
        corr_vals_one[idx] = corr_matrix_one[i, j]
        corr_vals_zero[idx] = corr_matrix_zero[i, j]
        same_vendor[idx] = (vendors[i] == vendors[j])
        delta_prod[idx] = delta[i] * delta[j]
        
    # 3. Headline Comparison
    avg_corr_same_one = np.mean(corr_vals_one[same_vendor])
    avg_corr_cross_one = np.mean(corr_vals_one[~same_vendor])
    avg_corr_same_zero = np.mean(corr_vals_zero[same_vendor])
    avg_corr_cross_zero = np.mean(corr_vals_zero[~same_vendor])
    
    print("\nTable 2: 2x2 Correlation Matrix (Average Pairwise Residual Correlation)")
    print("-" * 65)
    print(f"{'Pair Type':<25} | {'Dataset ONE (theta = 0.2)':<20} | {'Dataset ZERO (theta = 0.0)':<20}")
    print("-" * 65)
    print(f"{'Same Vendor Pairs':<25} | {avg_corr_same_one:<20.6f} | {avg_corr_same_zero:<20.6f}")
    print(f"{'Cross Vendor Pairs':<25} | {avg_corr_cross_one:<20.6f} | {avg_corr_cross_zero:<20.6f}")
    print("-" * 65)
    
    # 4. Regression Analysis
    beta_one, se_one = run_regression(corr_vals_one, same_vendor, delta_prod)
    beta_zero, se_zero = run_regression(corr_vals_zero, same_vendor, delta_prod)
    
    print("\nTable 3: Regression Results (Dependent Variable: Pairwise Residual Correlation)")
    print("-" * 75)
    print(f"{'Coefficient':<25} | {'Dataset ONE (theta = 0.2)':<22} | {'Dataset ZERO (theta = 0.0)':<22}")
    print("-" * 75)
    labels = ["b0 (Intercept)", "b1 (SameVendor)", "b2 (SameVendor x d_i*d_j)", "b3 (d_i*d_j)"]
    for i, label in enumerate(labels):
        print(f"{label:<25} | {beta_one[i]:>9.5f} (SE: {se_one[i]:.5f}) | {beta_zero[i]:>9.5f} (SE: {se_zero[i]:.5f})")
    print("-" * 75)
    
    # 5. Binned Scatter Plot for Dataset ONE
    # Bin by delta_i * delta_j product
    num_bins = 15
    bins = np.linspace(delta_prod.min(), delta_prod.max(), num_bins + 1)
    
    # Prepare same-vendor and cross-vendor data
    sv_delta_prod = delta_prod[same_vendor]
    sv_corr = corr_vals_one[same_vendor]
    cv_delta_prod = delta_prod[~same_vendor]
    cv_corr = corr_vals_one[~same_vendor]
    
    sv_bin_centers = []
    sv_bin_means = []
    cv_bin_centers = []
    cv_bin_means = []
    
    for i in range(num_bins):
        # Same vendor
        sv_mask = (sv_delta_prod >= bins[i]) & (sv_delta_prod < bins[i+1])
        if np.sum(sv_mask) > 0:
            sv_bin_centers.append(np.mean(sv_delta_prod[sv_mask]))
            sv_bin_means.append(np.mean(sv_corr[sv_mask]))
            
        # Cross vendor
        cv_mask = (cv_delta_prod >= bins[i]) & (cv_delta_prod < bins[i+1])
        if np.sum(cv_mask) > 0:
            cv_bin_centers.append(np.mean(cv_delta_prod[cv_mask]))
            cv_bin_means.append(np.mean(cv_corr[cv_mask]))
            
    # Plotting
    plt.figure(figsize=(8, 5))
    plt.plot(sv_bin_centers, sv_bin_means, 'o-', color='darkblue', label='Same-Vendor Pairs')
    plt.plot(cv_bin_centers, cv_bin_means, 's-', color='darkred', label='Cross-Vendor Pairs')
    plt.xlabel('Product of Usages ($\\delta_i \\delta_j$)')
    plt.ylabel('Average Residual Correlation')
    plt.title('Binned Scatter Plot: Pair Correlation vs. Usage Product (Dataset ONE)')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    
    os.makedirs('plots', exist_ok=True)
    plt.savefig('plots/part2_binned_scatter.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved binned scatter plot to plots/part2_binned_scatter.png")
    
    # Save reports
    with open('data/part2_report.txt', 'w') as f:
        f.write("Table 2: 2x2 Correlation Matrix (Average Pairwise Residual Correlation)\n")
        f.write("-" * 65 + "\n")
        f.write(f"{'Pair Type':<25} | {'Dataset ONE (theta = 0.2)':<20} | {'Dataset ZERO (theta = 0.0)':<20}\n")
        f.write("-" * 65 + "\n")
        f.write(f"{'Same Vendor Pairs':<25} | {avg_corr_same_one:<20.6f} | {avg_corr_same_zero:<20.6f}\n")
        f.write(f"{'Cross Vendor Pairs':<25} | {avg_corr_cross_one:<20.6f} | {avg_corr_cross_zero:<20.6f}\n")
        f.write("-" * 65 + "\n\n")
        
        f.write("Table 3: Regression Results\n")
        f.write("-" * 75 + "\n")
        f.write(f"{'Coefficient':<25} | {'Dataset ONE (theta = 0.2)':<22} | {'Dataset ZERO (theta = 0.0)':<22}\n")
        f.write("-" * 75 + "\n")
        for i, label in enumerate(labels):
            f.write(f"{label:<25} | {beta_one[i]:>9.5f} (SE: {se_one[i]:.5f}) | {beta_zero[i]:>9.5f} (SE: {se_zero[i]:.5f})\n")
        f.write("-" * 75 + "\n")

if __name__ == "__main__":
    run_part2()
