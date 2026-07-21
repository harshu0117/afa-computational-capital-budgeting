# [Human-Authored]
# Quality gap grid for sweep
import numpy as np
GAP_GRID = np.linspace(0.0, 0.05, 21)
BASE_BENEFIT_B = 0.18

# [AI-Generated]
import os
import sys
import matplotlib.pyplot as plt

# Add current directory to path to ensure simulation_core is importable
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from run_part4 import run_equilibrium

def run_part8():
    print("=== PART 8: The Tipping Boundary and Interior Frontier ===")
    
    # 1. Interior rerun (Gap = 0.01, Benefit A = 0.19, Benefit B = 0.18)
    print("Running interior rerun (A=0.19, B=0.18, Gap=0.01)...")
    res_interior_base = run_equilibrium(benefit_A=0.19, benefit_B=0.18)
    
    # 2. Quality Gap Sweep (21 runs: gap from 0.000 to 0.050)
    print("Running 21-run quality gap sweep...")
    shares_A = []
    usages_A = []
    usages_B = []
    sys_vars = []
    
    for gap in GAP_GRID:
        benefit_A = BASE_BENEFIT_B + gap
        res = run_equilibrium(benefit_A=benefit_A, benefit_B=BASE_BENEFIT_B)
        
        shares_A.append(res['s_A'])
        usages_A.append(res['delta_A'])
        usages_B.append(res['delta_B'])
        sys_var = 0.2 * (res['D_A']**2 + res['D_B']**2)
        sys_vars.append(sys_var)
        
    shares_A = np.array(shares_A)
    sys_vars = np.array(sys_vars)
    
    # 3. Theoretical Line Calculation
    # Theoretical tipping kink sits where gap = 0.10 * delta*
    # At gap=0, delta* approx 0.18. So kink is at gap approx 0.018.
    delta_star_base = 0.18 / (1.0 + 0.10 * 0.5) # approx 0.1714 or 0.18
    kink_gap = 0.10 * delta_star_base
    
    # Theoretical share of A: s_A = 0.5 + gap / (2 * 0.10 * delta*) clipped at 1.0
    theory_shares = np.clip(0.5 + GAP_GRID / (2.0 * 0.10 * delta_star_base), 0.5, 1.0)
    
    # 4. Frontier Experiment (Done Right, inside interior)
    # Start at Gap 0.01 (A=0.19, B=0.18), raise A by 0.005 to 0.195
    print("Running interior frontier experiment (A=0.190 -> 0.195, B=0.180)...")
    res_front_before = run_equilibrium(benefit_A=0.190, benefit_B=0.180)
    res_front_after = run_equilibrium(benefit_A=0.195, benefit_B=0.180,
                                      start_s_A=res_front_before['s_A'],
                                      start_delta_A=res_front_before['delta_A'],
                                      start_delta_B=res_front_before['delta_B'])
    
    sys_var_before = 0.2 * (res_front_before['D_A']**2 + res_front_before['D_B']**2)
    sys_var_after = 0.2 * (res_front_after['D_A']**2 + res_front_after['D_B']**2)
    
    # Print Table
    print("\nTable 9: Interior Frontier Experiment (Before vs. After 0.005 Model Improvement)")
    print("=" * 80)
    print(f"{'Quantity':<30} | {'Before (A=0.190, B=0.180)':<22} | {'After (A=0.195, B=0.180)':<22}")
    print("=" * 80)
    print(f"{'Vendor A Share':<30} | {res_front_before['s_A']*100:>20.2f}% | {res_front_after['s_A']*100:>20.2f}%")
    print(f"{'Vendor A Usage (delta_A)':<30} | {res_front_before['delta_A']:>21.6f} | {res_front_after['delta_A']:>21.6f}")
    print(f"{'Vendor B Usage (delta_B)':<30} | {res_front_before['delta_B']:>21.6f} | {res_front_after['delta_B']:>21.6f}")
    print(f"{'Vendor A Crowd Size (D_A)':<30} | {res_front_before['D_A']:>21.6f} | {res_front_after['D_A']:>21.6f}")
    print(f"{'Vendor B Crowd Size (D_B)':<30} | {res_front_before['D_B']:>21.6f} | {res_front_after['D_B']:>21.6f}")
    print(f"{'Total Systematic Variance':<30} | {sys_var_before:>21.6f} | {sys_var_after:>21.6f}")
    print("=" * 80)
    
    # Plotting: Two-panel figure (Share vs Gap and Systematic Variance vs Gap)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Panel 1: Share vs Gap
    ax1.plot(GAP_GRID, shares_A * 100, 'o', color='darkblue', label='Simulated Vendor A Share')
    ax1.plot(GAP_GRID, theory_shares * 100, '--', color='red', label='Theoretical Prediction')
    ax1.axvline(x=kink_gap, color='gray', linestyle=':', label=f'Tipping Boundary (Gap ≈ {kink_gap:.3f})')
    ax1.set_xlabel('Vendor A Quality Advantage / Gap')
    ax1.set_ylabel("Vendor A's Market Share (%)")
    ax1.set_title("Vendor A Market Share vs. Quality Advantage (Tipping Kink)")
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.legend()
    
    # Panel 2: Systematic Variance vs Gap
    ax2.plot(GAP_GRID, sys_vars, 's-', color='darkgreen', label='Total Systematic Risk 0.2*(DA^2 + DB^2)')
    ax2.axvline(x=kink_gap, color='gray', linestyle=':', label='Tipping Boundary')
    ax2.set_xlabel('Vendor A Quality Advantage / Gap')
    ax2.set_ylabel('Total Systematic Risk')
    ax2.set_title('Market-Wide Systematic Risk Concentration')
    ax2.grid(True, linestyle='--', alpha=0.5)
    ax2.legend()
    
    plt.tight_layout()
    os.makedirs('plots', exist_ok=True)
    plt.savefig('plots/part8_tipping_boundary.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved tipping boundary and risk figures to plots/part8_tipping_boundary.png")
    
    # Save Report
    os.makedirs('data', exist_ok=True)
    with open('data/part8_report.txt', 'w') as f:
        f.write("Table 9: Interior Frontier Experiment (Before vs. After 0.005 Model Improvement)\n")
        f.write("=" * 80 + "\n")
        f.write(f"{'Quantity':<30} | {'Before (A=0.190, B=0.180)':<22} | {'After (A=0.195, B=0.180)':<22}\n")
        f.write("=" * 80 + "\n")
        f.write(f"{'Vendor A Share':<30} | {res_front_before['s_A']*100:>20.2f}% | {res_front_after['s_A']*100:>20.2f}%\n")
        f.write(f"{'Vendor A Usage (delta_A)':<30} | {res_front_before['delta_A']:>21.6f} | {res_front_after['delta_A']:>21.6f}\n")
        f.write(f"{'Vendor B Usage (delta_B)':<30} | {res_front_before['delta_B']:>21.6f} | {res_front_after['delta_B']:>21.6f}\n")
        f.write(f"{'Vendor A Crowd Size (D_A)':<30} | {res_front_before['D_A']:>21.6f} | {res_front_after['D_A']:>21.6f}\n")
        f.write(f"{'Vendor B Crowd Size (D_B)':<30} | {res_front_before['D_B']:>21.6f} | {res_front_after['D_B']:>21.6f}\n")
        f.write(f"{'Total Systematic Variance':<30} | {sys_var_before:>21.6f} | {sys_var_after:>21.6f}\n")
        f.write("=" * 80 + "\n")

if __name__ == "__main__":
    run_part8()
