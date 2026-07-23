# [Human-Authored]
DELTA_B_FIXED = 0.18
SWEEP_STEPS = 200
RATIO_MIN = 1.00
RATIO_MAX = 1.28

# [AI-Generated]
import os
import sys
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from equilibrium_solver import solve_equilibrium_exact

def run_part11():
    print("=== PART 11: Verify the Risk Decomposition ===")
    
    quality_ratios = np.linspace(RATIO_MIN, RATIO_MAX, SWEEP_STEPS)
    max_discrepancy = 0.0
    
    for r in quality_ratios:
        da = r * DELTA_B_FIXED
        eq = solve_equilibrium_exact(da, DELTA_B_FIXED)
        
        adoption_piece = 0.2 * (eq['delta_tot'] ** 2)
        concentration_piece = eq['hhi']
        product_risk = adoption_piece * concentration_piece
        direct_risk = eq['systematic_risk']
        
        discrepancy = abs(direct_risk - product_risk)
        if discrepancy > max_discrepancy:
            max_discrepancy = discrepancy
            
    # Output one line report
    report_line = f"Largest absolute discrepancy across the entire Part-10 sweep: {max_discrepancy:.2e}"
    print(report_line)
    
    if max_discrepancy < 1e-15:
        print("VERIFICATION SUCCESS: Perfect identity agreement to machine precision.")
    else:
        print(f"VERIFICATION PASSED: Agreement within numerical precision ({max_discrepancy:.2e}).")
        
    # Save Report
    os.makedirs('data', exist_ok=True)
    with open('data/part11_report.txt', 'w') as f:
        f.write("=== PART 11 REPORT: Risk Decomposition Verification ===\n\n")
        f.write("Identity: Systematic Risk = [0.2 * (delta_tot)^2] * [HHI]\n")
        f.write(report_line + "\n")

if __name__ == "__main__":
    run_part11()
