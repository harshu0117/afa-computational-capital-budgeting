# [Human-Authored]
# No separate parameters required here (loaded from simulation_core.py)

# [AI-Generated]
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

def run_equilibrium(benefit_A, benefit_B, start_s_A=0.5, start_delta_A=0.1, start_delta_B=0.1, max_iter=1000, tol=1e-6):
    """
    Runs the equilibrium convergence loop for a given set of benefit rates.
    """
    s_A = start_s_A
    delta_A = start_delta_A
    delta_B = start_delta_B
    
    s_A_history = [s_A]
    delta_A_history = [delta_A]
    delta_B_history = [delta_B]
    
    for i in range(max_iter):
        s_B = 1.0 - s_A
        
        # (i) Compute crowd size
        D_A = s_A * delta_A
        D_B = s_B * delta_B
        
        # (ii) Compute best usage (restricted to [0.0, 0.4] per definitions)
        delta_A_new = max(0.0, min(0.4, benefit_A - 0.10 * D_A))
        delta_B_new = max(0.0, min(0.4, benefit_B - 0.10 * D_B))
        
        # Compute achieved value
        value_A = benefit_A * delta_A_new - 0.5 * (delta_A_new ** 2) - 0.10 * delta_A_new * D_A
        value_B = benefit_B * delta_B_new - 0.5 * (delta_B_new ** 2) - 0.10 * delta_B_new * D_B
        
        s_A_old = s_A
        delta_A_old = delta_A
        delta_B_old = delta_B
        
        # (iii) Move 5% of firms toward the vendor offering higher value
        if value_A > value_B:
            s_A = min(1.0, s_A + 0.05)
        elif value_B > value_A:
            s_A = max(0.0, s_A - 0.05)
            
        delta_A = delta_A_new
        delta_B = delta_B_new
        
        s_A_history.append(s_A)
        delta_A_history.append(delta_A)
        delta_B_history.append(delta_B)
        
        # Check convergence
        change = max(abs(s_A - s_A_old), abs(delta_A - delta_A_old), abs(delta_B - delta_B_old))
        if change < tol:
            break
            
    return {
        's_A': s_A,
        's_B': 1.0 - s_A,
        'delta_A': delta_A,
        'delta_B': delta_B,
        'D_A': s_A * delta_A,
        'D_B': (1.0 - s_A) * delta_B,
        's_A_history': s_A_history,
        'iterations': len(s_A_history) - 1
    }

def run_part4():
    print("=== PART 4: A Tiny Equilibrium ===")
    
    # 1. Iterate to a fixed point for initial rates
    print("Running initial episode (Benefit rates: A=0.20, B=0.18)...")
    res_initial = run_equilibrium(benefit_A=0.20, benefit_B=0.18)
    
    # 2. Re-converge after improving vendor A
    print("Running experiment episode (Benefit rates: A=0.24, B=0.18)...")
    res_experiment = run_equilibrium(benefit_A=0.24, benefit_B=0.18, 
                                     start_s_A=res_initial['s_A'], 
                                     start_delta_A=res_initial['delta_A'], 
                                     start_delta_B=res_initial['delta_B'])
    
    # Compute systematic variance = 0.2 * (D_A^2 + D_B^2)
    sys_var_initial = 0.2 * (res_initial['D_A']**2 + res_initial['D_B']**2)
    sys_var_experiment = 0.2 * (res_experiment['D_A']**2 + res_experiment['D_B']**2)
    
    # Print table
    print("\nTable 5: Equilibrium Results Before and After Improvement")
    print("-" * 80)
    print(f"{'Quantity':<30} | {'Before (A=0.20)':<22} | {'After (A=0.24)':<22}")
    print("-" * 80)
    print(f"{'Vendor A Share':<30} | {res_initial['s_A']*100:>20.2f}% | {res_experiment['s_A']*100:>20.2f}%")
    print(f"{'Vendor A Usage (delta_A)':<30} | {res_initial['delta_A']:>21.6f} | {res_experiment['delta_A']:>21.6f}")
    print(f"{'Vendor B Usage (delta_B)':<30} | {res_initial['delta_B']:>21.6f} | {res_experiment['delta_B']:>21.6f}")
    print(f"{'Vendor A Crowd Size (D_A)':<30} | {res_initial['D_A']:>21.6f} | {res_experiment['D_A']:>21.6f}")
    print(f"{'Vendor B Crowd Size (D_B)':<30} | {res_initial['D_B']:>21.6f} | {res_experiment['D_B']:>21.6f}")
    print(f"{'Total Systematic Variance':<30} | {sys_var_initial:>21.6f} | {sys_var_experiment:>21.6f}")
    print("-" * 80)
    
    # Plotting convergence path
    plt.figure(figsize=(10, 6))
    
    # Plot initial episode
    plt.plot(res_initial['s_A_history'], color='blue', label='Episode 1: A=0.20, B=0.18')
    
    # Plot experiment episode (offsetting the x-axis to follow the first)
    offset = len(res_initial['s_A_history']) - 1
    plt.plot(range(offset, offset + len(res_experiment['s_A_history'])), 
             res_experiment['s_A_history'], color='green', linestyle='--', label='Episode 2: A=0.24, B=0.18')
    
    plt.xlabel('Iteration')
    plt.ylabel("Vendor A's Share of Firms (s_A)")
    plt.title("Convergence Path of Vendor A's Share Across Episodes")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    
    os.makedirs('plots', exist_ok=True)
    plt.savefig('plots/part4_convergence_path.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved convergence path plot to plots/part4_convergence_path.png")
    
    # Save report
    with open('data/part4_report.txt', 'w') as f:
        f.write("Table 5: Equilibrium Results Before and After Improvement\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'Quantity':<30} | {'Before (A=0.20)':<22} | {'After (A=0.24)':<22}\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'Vendor A Share':<30} | {res_initial['s_A']*100:>20.2f}% | {res_experiment['s_A']*100:>20.2f}%\n")
        f.write(f"{'Vendor A Usage (delta_A)':<30} | {res_initial['delta_A']:>21.6f} | {res_experiment['delta_A']:>21.6f}\n")
        f.write(f"{'Vendor B Usage (delta_B)':<30} | {res_initial['delta_B']:>21.6f} | {res_experiment['delta_B']:>21.6f}\n")
        f.write(f"{'Vendor A Crowd Size (D_A)':<30} | {res_initial['D_A']:>21.6f} | {res_experiment['D_A']:>21.6f}\n")
        f.write(f"{'Vendor B Crowd Size (D_B)':<30} | {res_initial['D_B']:>21.6f} | {res_experiment['D_B']:>21.6f}\n")
        f.write(f"{'Total Systematic Variance':<30} | {sys_var_initial:>21.6f} | {sys_var_experiment:>21.6f}\n")
        f.write("-" * 80 + "\n")

if __name__ == "__main__":
    run_part4()
