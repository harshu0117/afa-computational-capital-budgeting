# [Human-Authored]
DELTA_B_FIXED = 0.18
SWEEP_STEPS = 200
RATIO_MIN = 1.00
RATIO_MAX = 1.28
FRONTIER_DELTA_A_BEFORE = 0.190
FRONTIER_DELTA_A_AFTER = 0.195

# [AI-Generated]
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from equilibrium_solver import solve_equilibrium_exact

def run_part10():
    print("=== PART 10: Redo the Sweep and the Frontier Experiment ===")
    
    # 1. Quality Ratio Sweep
    quality_ratios = np.linspace(RATIO_MIN, RATIO_MAX, SWEEP_STEPS)
    leader_shares = []
    total_delegations = []
    hhi_indices = []
    systematic_risks = []
    
    for r in quality_ratios:
        da = r * DELTA_B_FIXED
        eq = solve_equilibrium_exact(da, DELTA_B_FIXED)
        leader_shares.append(eq['s_a'])
        total_delegations.append(eq['delta_tot'])
        hhi_indices.append(eq['hhi'])
        systematic_risks.append(eq['systematic_risk'])
        
    leader_shares = np.array(leader_shares)
    total_delegations = np.array(total_delegations)
    hhi_indices = np.array(hhi_indices)
    systematic_risks = np.array(systematic_risks)
    
    # 2. Frontier Experiment
    eq_before = solve_equilibrium_exact(FRONTIER_DELTA_A_BEFORE, DELTA_B_FIXED)
    eq_after = solve_equilibrium_exact(FRONTIER_DELTA_A_AFTER, DELTA_B_FIXED)
    
    share_before = eq_before['s_a'] * 100.0
    share_after = eq_after['s_a'] * 100.0
    share_pct_change = (eq_after['s_a'] - eq_before['s_a']) / eq_before['s_a'] * 100.0
    
    tot_before = eq_before['delta_tot']
    tot_after = eq_after['delta_tot']
    tot_pct_change = (tot_after - tot_before) / tot_before * 100.0
    adoption_pct_change = ((tot_after**2) - (tot_before**2)) / (tot_before**2) * 100.0
    
    hhi_before = eq_before['hhi']
    hhi_after = eq_after['hhi']
    hhi_pct_change = (hhi_after - hhi_before) / hhi_before * 100.0
    
    risk_before = eq_before['systematic_risk']
    risk_after = eq_after['systematic_risk']
    risk_pct_change = (risk_after - risk_before) / risk_before * 100.0
    
    print("\nTable 2: Frontier Experiment Results (Delta_A 0.190 -> 0.195, Delta_B = 0.180)")
    print("=" * 95)
    print(f"{'Quantity':<35} | {'Before (Delta_A=0.190)':<22} | {'After (Delta_A=0.195)':<22} | {'Pct Change':<12}")
    print("=" * 95)
    print(f"{'Leader Share (s_A)':<35} | {share_before:>21.4f}% | {share_after:>21.4f}% | {share_pct_change:>11.2f}%")
    print(f"{'Total Delegation (delta_tot)':<35} | {tot_before:>22.8f} | {tot_after:>22.8f} | {tot_pct_change:>11.2f}%")
    print(f"{'Adoption Component (0.2*delta_tot^2)':<35} | {eq_before['adoption_risk']:>22.8f} | {eq_after['adoption_risk']:>22.8f} | {adoption_pct_change:>11.2f}%")
    print(f"{'Concentration Component (HHI)':<35} | {hhi_before:>22.8f} | {hhi_after:>22.8f} | {hhi_pct_change:>11.2f}%")
    print(f"{'Total Systematic Risk':<35} | {risk_before:>22.8f} | {risk_after:>22.8f} | {risk_pct_change:>11.2f}%")
    print("=" * 95)
    print("\nSystematic Risk Change Decomposition:")
    print(f"  - Total Systematic Risk Increase: {risk_pct_change:.2f}%")
    print(f"  - Contribution from Higher Delegation (Adoption): ~{adoption_pct_change:.2f} percentage points")
    print(f"  - Contribution from Higher Concentration (HHI):   ~{hhi_pct_change:.2f} percentage points")
    
    # 3. Visualizations
    os.makedirs('plots', exist_ok=True)
    
    # Figure 1: Leader Share vs Quality Ratio
    plt.figure(figsize=(8, 5))
    plt.plot(quality_ratios, leader_shares * 100, color='#1f77b4', linewidth=2.5, label='Leader Share (s_A)')
    plt.axvline(x=1.10, color='red', linestyle='--', linewidth=1.5, label='Tipping Threshold (1.10)')
    plt.xlabel('Quality Ratio (Delta_A / Delta_B)', fontsize=11)
    plt.ylabel("Leader's Market Share (%)", fontsize=11)
    plt.title("Figure 1: Leader Market Share vs. Quality Ratio", fontsize=12, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.savefig('plots/part10_leader_share.png', dpi=300)
    plt.close()
    
    # Figure 2: Systematic Risk vs Quality Ratio
    plt.figure(figsize=(8, 5))
    plt.plot(quality_ratios, systematic_risks, color='#2ca02c', linewidth=2.5, label='Systematic Risk')
    plt.axvline(x=1.10, color='red', linestyle='--', linewidth=1.5, label='Tipping Threshold (1.10)')
    plt.xlabel('Quality Ratio (Delta_A / Delta_B)', fontsize=11)
    plt.ylabel('Total Systematic Risk', fontsize=11)
    plt.title('Figure 2: Market-Wide Systematic Risk vs. Quality Ratio', fontsize=12, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.savefig('plots/part10_systematic_risk.png', dpi=300)
    plt.close()
    
    # Combined Two-Panel Figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
    ax1.plot(quality_ratios, leader_shares * 100, color='#1f77b4', linewidth=2.5, label='Leader Share (s_A)')
    ax1.axvline(x=1.10, color='red', linestyle='--', linewidth=1.5, label='Tipping Threshold (1.10)')
    ax1.set_xlabel('Quality Ratio (Delta_A / Delta_B)', fontsize=11)
    ax1.set_ylabel("Leader's Market Share (%)", fontsize=11)
    ax1.set_title("Vendor Market Share (Smooth Interior & Tipping Jump)", fontsize=11, fontweight='bold')
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend(fontsize=10)
    
    ax2.plot(quality_ratios, systematic_risks, color='#2ca02c', linewidth=2.5, label='Systematic Risk')
    ax2.axvline(x=1.10, color='red', linestyle='--', linewidth=1.5, label='Tipping Threshold (1.10)')
    ax2.set_xlabel('Quality Ratio (Delta_A / Delta_B)', fontsize=11)
    ax2.set_ylabel('Total Systematic Risk', fontsize=11)
    ax2.set_title('Systematic Risk Expansion Across Quality Ratios', fontsize=11, fontweight='bold')
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.legend(fontsize=10)
    
    plt.tight_layout()
    plt.savefig('plots/part10_sweep_and_frontier.png', dpi=300)
    plt.close()
    print("Saved plots to plots/part10_leader_share.png, plots/part10_systematic_risk.png, and plots/part10_sweep_and_frontier.png")
    
    # Save Report
    os.makedirs('data', exist_ok=True)
    with open('data/part10_report.txt', 'w') as f:
        f.write("=== PART 10 REPORT: Sweep and Frontier Experiment ===\n\n")
        f.write("Table 2: Frontier Experiment Results (Delta_A 0.190 -> 0.195, Delta_B = 0.180)\n")
        f.write("=" * 95 + "\n")
        f.write(f"{'Quantity':<35} | {'Before (Delta_A=0.190)':<22} | {'After (Delta_A=0.195)':<22} | {'Pct Change':<12}\n")
        f.write("=" * 95 + "\n")
        f.write(f"{'Leader Share (s_A)':<35} | {share_before:>21.4f}% | {share_after:>21.4f}% | {share_pct_change:>11.2f}%\n")
        f.write(f"{'Total Delegation (delta_tot)':<35} | {tot_before:>22.8f} | {tot_after:>22.8f} | {tot_pct_change:>11.2f}%\n")
        f.write(f"{'Adoption Component (0.2*delta_tot^2)':<35} | {eq_before['adoption_risk']:>22.8f} | {eq_after['adoption_risk']:>22.8f} | {adoption_pct_change:>11.2f}%\n")
        f.write(f"{'Concentration Component (HHI)':<35} | {hhi_before:>22.8f} | {hhi_after:>22.8f} | {hhi_pct_change:>11.2f}%\n")
        f.write(f"{'Total Systematic Risk':<35} | {risk_before:>22.8f} | {risk_after:>22.8f} | {risk_pct_change:>11.2f}%\n")
        f.write("=" * 95 + "\n\n")
        f.write("Systematic Risk Change Decomposition:\n")
        f.write(f"  - Total Systematic Risk Increase: {risk_pct_change:.2f}%\n")
        f.write(f"  - Contribution from Higher Delegation (Adoption): ~{adoption_pct_change:.2f} percentage points\n")
        f.write(f"  - Contribution from Higher Concentration (HHI):   ~{hhi_pct_change:.2f} percentage points\n")

if __name__ == "__main__":
    run_part10()
