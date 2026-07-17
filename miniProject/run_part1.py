# [Human-Authored]
# No separate parameters required here (loaded from simulation_core.py)

# [AI-Generated]
import numpy as np
import os
import sys

# Add current directory to path to ensure simulation_core is importable
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from simulation_core import generate_market_data, THETA_ONE, THETA_ZERO

def run_part1():
    print("=== PART 1: Building the Fake Market ===")
    
    # Generate datasets
    data_one = generate_market_data(THETA_ONE)
    data_zero = generate_market_data(THETA_ZERO)
    
    # Verify assignments are identical
    vendors_match = np.array_equal(data_one['vendors'], data_zero['vendors'])
    delta_match = np.allclose(data_one['delta'], data_zero['delta'])
    beta_match = np.allclose(data_one['beta'], data_zero['beta'])
    shocks_match = np.allclose(data_one['m'], data_zero['m']) and \
                   np.allclose(data_one['eta_A'], data_zero['eta_A']) and \
                   np.allclose(data_one['eta_B'], data_zero['eta_B']) and \
                   np.allclose(data_one['epsilon'], data_zero['epsilon'])
    
    all_identical = vendors_match and delta_match and beta_match and shocks_match
    
    # Calculate stats
    num_firms = len(data_one['vendors'])
    num_days = len(data_one['m'])
    vendor_a_count = np.sum(data_one['vendors'] == 'A')
    vendor_b_count = np.sum(data_one['vendors'] == 'B')
    avg_delta = np.mean(data_one['delta'])
    avg_beta = np.mean(data_one['beta'])
    
    # Print report
    print("\nTable 1: Simulation Setup and Parameter Verification")
    print("-" * 55)
    print(f"{'Parameter':<30} | {'Value':<20}")
    print("-" * 55)
    print(f"{'Number of Firms (N)':<30} | {num_firms:<20}")
    print(f"{'Number of Trading Days (T)':<30} | {num_days:<20}")
    print(f"{'Vendor A Share':<30} | {vendor_a_count / num_firms * 100:.1f}% ({vendor_a_count} firms)")
    print(f"{'Vendor B Share':<30} | {vendor_b_count / num_firms * 100:.1f}% ({vendor_b_count} firms)")
    print(f"{'Average Usage (delta_i)':<30} | {avg_delta:.6f}")
    print(f"{'Average Beta (beta_i)':<30} | {avg_beta:.6f}")
    print("-" * 55)
    print(f"Verification: Both datasets were built from identical firm assignments: {all_identical}")
    print("-" * 55)
    
    # Save the generated datasets for Part 2
    os.makedirs('data', exist_ok=True)
    np.save('data/r_one.npy', data_one['r'])
    np.save('data/r_zero.npy', data_zero['r'])
    np.save('data/vendors.npy', data_one['vendors'])
    np.save('data/delta.npy', data_one['delta'])
    np.save('data/beta.npy', data_one['beta'])
    np.save('data/m.npy', data_one['m'])
    print("Saved return data and firm parameters to data/ directory.")
    
    # Save report text
    with open('data/part1_report.txt', 'w') as f:
        f.write("Table 1: Simulation Setup and Parameter Verification\n")
        f.write("-" * 55 + "\n")
        f.write(f"{'Parameter':<30} | {'Value':<20}\n")
        f.write("-" * 55 + "\n")
        f.write(f"{'Number of Firms (N)':<30} | {num_firms:<20}\n")
        f.write(f"{'Number of Trading Days (T)':<30} | {num_days:<20}\n")
        f.write(f"{'Vendor A Share':<30} | {vendor_a_count / num_firms * 100:.1f}% ({vendor_a_count} firms)\n")
        f.write(f"{'Vendor B Share':<30} | {vendor_b_count / num_firms * 100:.1f}% ({vendor_b_count} firms)\n")
        f.write(f"{'Average Usage (delta_i)':<30} | {avg_delta:.6f}\n")
        f.write(f"{'Average Beta (beta_i)':<30} | {avg_beta:.6f}\n")
        f.write("-" * 55 + "\n")
        f.write(f"Verification: Both datasets were built from identical firm assignments: {all_identical}\n")
        f.write("-" * 55 + "\n")

if __name__ == "__main__":
    run_part1()
