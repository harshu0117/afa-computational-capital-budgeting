# [Human-Authored]
GAMMA = 0.5
SIGMA_A_SQ = 1.0
THETA_GRID_NUM = 200
CHI_GRID_NUM = 200
THETA_RANGE = (0.01, 0.40)
CHI_RANGE = (0.5, 4.0)

THETA_TABLE_VALS = [0.05, 0.10, 0.20, 0.40]
CHI_TABLE_VALS = [0.5, 1.0, 2.0, 4.0]
CONTOUR_LEVELS = [1.01, 1.02, 1.05, 1.10, 1.20, 1.40]

# [AI-Generated]
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

def run_part12():
    print("=== PART 12: The Survival Region ===")
    
    # 1. Compute 2D Grid of Tipping Thresholds
    theta_vals = np.linspace(THETA_RANGE[0], THETA_RANGE[1], THETA_GRID_NUM)
    chi_vals = np.linspace(CHI_RANGE[0], CHI_RANGE[1], CHI_GRID_NUM)
    THETA, CHI = np.meshgrid(theta_vals, chi_vals)
    
    # k = gamma * theta * sigma_A^2 = 0.5 * theta
    K = GAMMA * THETA * SIGMA_A_SQ
    THRESHOLD = 1.0 + K / CHI
    
    # 2. Compute Table Values
    table_data = np.zeros((len(CHI_TABLE_VALS), len(THETA_TABLE_VALS)))
    for i, chi in enumerate(CHI_TABLE_VALS):
        for j, theta in enumerate(THETA_TABLE_VALS):
            k_val = GAMMA * theta * SIGMA_A_SQ
            table_data[i, j] = 1.0 + k_val / chi
            
    print("\nTable 3: Vendor Diversity Tipping Threshold Matrix (1 + k / chi)")
    print("=" * 70)
    header = f"{'Cost Curvature (chi)':<22} | " + " | ".join([f"theta={t:<5.2f}" for t in THETA_TABLE_VALS])
    print(header)
    print("=" * 70)
    for i, chi in enumerate(CHI_TABLE_VALS):
        row_str = f"chi = {chi:<16.1f} | " + " | ".join([f"{table_data[i, j]:^10.4f}" for j in range(len(THETA_TABLE_VALS))])
        print(row_str)
    print("=" * 70)
    print("Calibration Point: theta = 0.20, chi = 1.00 -> Tipping Threshold = 1.1000")
    
    # 3. Visualization: Contour Plot of Tipping Threshold
    os.makedirs('plots', exist_ok=True)
    plt.figure(figsize=(9, 6.5))
    
    # Contour fill & lines
    cf = plt.contourf(THETA, CHI, THRESHOLD, levels=50, cmap='viridis', alpha=0.85)
    cbar = plt.colorbar(cf)
    cbar.set_label('Tipping Threshold (1 + k / chi)', fontsize=11)
    
    cs = plt.contour(THETA, CHI, THRESHOLD, levels=CONTOUR_LEVELS, colors='white', linewidths=1.5)
    plt.clabel(cs, inline=True, fontsize=10, fmt='%.2f')
    
    # Mark calibration point (theta = 0.2, chi = 1.0)
    plt.plot(0.20, 1.00, marker='*', color='red', markersize=14, label='Calibration Point (theta=0.20, chi=1.00, Threshold=1.10)')
    
    plt.xlabel('AI Error Correlation Parameter (theta)', fontsize=11)
    plt.ylabel('Integration Cost Curvature (chi)', fontsize=11)
    plt.title('Figure 3: Survival Region of Dual Vendor Market Diversity', fontsize=12, fontweight='bold')
    plt.grid(True, linestyle=':', alpha=0.4, color='white')
    plt.legend(loc='upper left', fontsize=10)
    plt.tight_layout()
    
    plot_path = 'plots/part12_survival_region.png'
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"Saved survival region contour figure to {plot_path}")
    
    # 4. Save Text Report
    os.makedirs('data', exist_ok=True)
    with open('data/part12_report.txt', 'w') as f:
        f.write("=== PART 12 REPORT: The Survival Region ===\n\n")
        f.write("Table 3: Vendor Diversity Tipping Threshold Matrix (1 + k / chi)\n")
        f.write("=" * 70 + "\n")
        f.write(header + "\n")
        f.write("=" * 70 + "\n")
        for i, chi in enumerate(CHI_TABLE_VALS):
            row_str = f"chi = {chi:<16.1f} | " + " | ".join([f"{table_data[i, j]:^10.4f}" for j in range(len(THETA_TABLE_VALS))])
            f.write(row_str + "\n")
        f.write("=" * 70 + "\n\n")
        f.write("Economic Interpretation:\n")
        f.write("Thresholds range from 1.006 (weakly correlated errors theta=0.05, expensive integration chi=4.0) ")
        f.write("to 1.400 (strongly correlated errors theta=0.40, cheap integration chi=0.5).\n")
        f.write("Vendor diversity is most fragile exactly where AI errors are least correlated, ")
        f.write("and most robust where AI errors are most correlated.\n")

if __name__ == "__main__":
    run_part12()
