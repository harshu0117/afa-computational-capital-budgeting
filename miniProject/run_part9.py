# [Human-Authored]
DELTA_B_BASE = 0.18
RATIOS_TO_TEST = [
    ("Interior", 0.190, 0.180),   # Quality ratio 1.0556 < 1.10
    ("Boundary", 0.198, 0.180),   # Quality ratio 1.1000 = 1.10
    ("Tipped", 0.216, 0.180)      # Quality ratio 1.2000 > 1.10
]

# [AI-Generated]
import os
import sys
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from equilibrium_solver import solve_equilibrium_exact, solve_equilibrium_iterative

def run_part9():
    print("=== PART 9: Solve the Equilibrium Exactly ===")
    
    table_rows = []
    max_discrepancy = 0.0
    
    for regime, da, db in RATIOS_TO_TEST:
        exact = solve_equilibrium_exact(da, db)
        it = solve_equilibrium_iterative(da, db)
        
        diff_sa = abs(exact['s_a'] - it['s_a'])
        diff_Da = abs(exact['D_a'] - it['D_a'])
        diff_Db = abs(exact['D_b'] - it['D_b'])
        diff_tot = abs(exact['delta_tot'] - it['delta_tot'])
        diff_hhi = abs(exact['hhi'] - it['hhi'])
        diff_risk = abs(exact['systematic_risk'] - it['systematic_risk'])
        
        local_max = max(diff_sa, diff_Da, diff_Db, diff_tot, diff_hhi, diff_risk)
        if local_max > max_discrepancy:
            max_discrepancy = local_max
            
        table_rows.append({
            'regime': regime,
            'da': da,
            'db': db,
            'ratio': exact['quality_ratio'],
            'exact_sa': exact['s_a'],
            'iter_sa': it['s_a'],
            'diff_sa': diff_sa,
            'exact_tot': exact['delta_tot'],
            'iter_tot': it['delta_tot'],
            'exact_hhi': exact['hhi'],
            'iter_hhi': it['hhi'],
            'exact_risk': exact['systematic_risk'],
            'iter_risk': it['systematic_risk']
        })
        
    print("\nTable 1: Part 9 Equilibrium Verification (Exact Formula vs. Iterative Solver)")
    print("=" * 110)
    print(f"{'Regime':<10} | {'Quality Ratio':<14} | {'Quantity':<18} | {'Formula Value':<20} | {'Iterative Value':<20} | {'Abs Diff':<12}")
    print("=" * 110)
    for r in table_rows:
        print(f"{r['regime']:<10} | {r['ratio']:<14.6f} | {'Leader Share (s_A)':<18} | {r['exact_sa']:<20.10f} | {r['iter_sa']:<20.10f} | {r['diff_sa']:<12.2e}")
        print(f"{'':<10} | {'':<14} | {'Total Delegation':<18} | {r['exact_tot']:<20.10f} | {r['iter_tot']:<20.10f} | {abs(r['exact_tot'] - r['iter_tot']):<12.2e}")
        print(f"{'':<10} | {'':<14} | {'HHI Index':<18} | {r['exact_hhi']:<20.10f} | {r['iter_hhi']:<20.10f} | {abs(r['exact_hhi'] - r['iter_hhi']):<12.2e}")
        print(f"{'':<10} | {'':<14} | {'Systematic Risk':<18} | {r['exact_risk']:<20.10f} | {r['iter_risk']:<20.10f} | {abs(r['exact_risk'] - r['iter_risk']):<12.2e}")
        print("-" * 110)
        
    print(f"\nMaximum absolute discrepancy across all quantities and regimes: {max_discrepancy:.2e}")
    if max_discrepancy < 1e-8:
        print("SUCCESS: Exact agreement certified to at least 8 decimal places.")
    else:
        print("WARNING: Discrepancy exceeds tolerance 1e-8.")
        
    # Save output report
    os.makedirs('data', exist_ok=True)
    with open('data/part9_report.txt', 'w') as f:
        f.write("=== PART 9 REPORT: Exact Solution vs Iterative Solver Verification ===\n")
        f.write(f"Maximum absolute discrepancy: {max_discrepancy:.2e}\n\n")
        f.write("Table 1: Part 9 Equilibrium Verification\n")
        f.write("=" * 110 + "\n")
        f.write(f"{'Regime':<10} | {'Quality Ratio':<14} | {'Quantity':<18} | {'Formula Value':<20} | {'Iterative Value':<20} | {'Abs Diff':<12}\n")
        f.write("=" * 110 + "\n")
        for r in table_rows:
            f.write(f"{r['regime']:<10} | {r['ratio']:<14.6f} | {'Leader Share (s_A)':<18} | {r['exact_sa']:<20.10f} | {r['iter_sa']:<20.10f} | {r['diff_sa']:<12.2e}\n")
            f.write(f"{'':<10} | {'':<14} | {'Total Delegation':<18} | {r['exact_tot']:<20.10f} | {r['iter_tot']:<20.10f} | {abs(r['exact_tot'] - r['iter_tot']):<12.2e}\n")
            f.write(f"{'':<10} | {'':<14} | {'HHI Index':<18} | {r['exact_hhi']:<20.10f} | {r['iter_hhi']:<20.10f} | {abs(r['exact_hhi'] - r['iter_hhi']):<12.2e}\n")
            f.write(f"{'':<10} | {'':<14} | {'Systematic Risk':<18} | {r['exact_risk']:<20.10f} | {r['iter_risk']:<20.10f} | {abs(r['exact_risk'] - r['iter_risk']):<12.2e}\n")
            f.write("-" * 110 + "\n")

if __name__ == "__main__":
    run_part9()
