# [Human-Authored]
# No separate parameters required here (loaded from simulation_core.py)

# [AI-Generated]
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

# Add current directory to path to ensure simulation_core is importable
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from simulation_core import generate_market_data, THETA_ONE, NUM_FIRMS, NUM_DAYS, VENDOR_A_COUNT
from run_part2 import calculate_residuals

def run_part3():
    print("=== PART 3: Event Days and Rolling Comovement ===")
    
    # 1. Pick 10 evenly spaced event days for vendor A
    # With T = 1000, spacing them by 100 days from day 50 to 950
    event_days = np.linspace(50, 950, 10, dtype=int)
    print(f"Vendor A event days selected: {event_days}")
    
    # Rebuild dataset ONE with 5x shocks for vendor A on event days
    data_event = generate_market_data(THETA_ONE, event_days_A=event_days, event_sd_factor=5.0)
    
    # Calculate residuals
    residuals = calculate_residuals(data_event['r'], data_event['m'])
    
    # Separate vendor A (0-299) and vendor B (300-499) residuals
    res_A = residuals[:, :VENDOR_A_COUNT] # shape (1000, 300)
    res_B = residuals[:, VENDOR_A_COUNT:] # shape (1000, 200)
    
    # 2. Compute rolling 11-day correlation for same-vendor A and B pairs
    rolling_comove_A = np.zeros(NUM_DAYS)
    rolling_comove_B = np.zeros(NUM_DAYS)
    
    triu_idx_A = np.triu_indices(VENDOR_A_COUNT, k=1)
    triu_idx_B = np.triu_indices(NUM_FIRMS - VENDOR_A_COUNT, k=1)
    
    print("Computing rolling 11-day pairwise correlation matrix...")
    for t in range(5, NUM_DAYS - 5):
        # Vendor A
        window_A = res_A[t-5:t+6, :]
        corr_A = np.corrcoef(window_A, rowvar=False)
        rolling_comove_A[t] = np.mean(corr_A[triu_idx_A])
        
        # Vendor B
        window_B = res_B[t-5:t+6, :]
        corr_B = np.corrcoef(window_B, rowvar=False)
        rolling_comove_B[t] = np.mean(corr_B[triu_idx_B])
        
    # 3. Pick 10 placebo days (random non-event days)
    np.random.seed(42)
    non_event_days = [d for d in range(5, NUM_DAYS - 5) if d not in event_days]
    placebo_days = np.random.choice(non_event_days, 10, replace=False)
    print(f"Placebo days selected: {placebo_days}")
    
    # Calculate average comovement for different windows
    # Event days
    ev_comove_A = np.mean(rolling_comove_A[event_days])
    ev_comove_B = np.mean(rolling_comove_B[event_days])
    
    # Placebo days
    pl_comove_A = np.mean(rolling_comove_A[placebo_days])
    pl_comove_B = np.mean(rolling_comove_B[placebo_days])
    
    # Other days (excluding event and placebo days)
    other_days = [d for d in range(5, NUM_DAYS - 5) if d not in event_days and d not in placebo_days]
    oth_comove_A = np.mean(rolling_comove_A[other_days])
    oth_comove_B = np.mean(rolling_comove_B[other_days])
    
    print("\nTable 4: Comovement in Event vs. Placebo Windows")
    print("-" * 65)
    print(f"{'Window Type':<20} | {'Vendor A Pairs':<18} | {'Vendor B Pairs (Control)':<22}")
    print("-" * 65)
    print(f"{'Event Windows':<20} | {ev_comove_A:<18.6f} | {ev_comove_B:<22.6f}")
    print(f"{'Placebo Windows':<20} | {pl_comove_A:<18.6f} | {pl_comove_B:<22.6f}")
    print(f"{'All Other Days':<20} | {oth_comove_A:<18.6f} | {oth_comove_B:<22.6f}")
    print("-" * 65)
    
    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(range(5, NUM_DAYS-5), rolling_comove_A[5:NUM_DAYS-5], color='darkblue', label='Vendor A Same-Vendor Comovement')
    
    # Mark event days
    for idx, ed in enumerate(event_days):
        plt.axvline(x=ed, color='red', linestyle='--', alpha=0.7, label='Vendor A Event Days' if idx == 0 else "")
        
    plt.xlabel('Trading Day (t)')
    plt.ylabel('Average 11-Day Rolling Residual Correlation')
    plt.title("Rolling Same-Vendor Comovement Over Time (Vendor A vs. Event Days)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    
    os.makedirs('plots', exist_ok=True)
    plt.savefig('plots/part3_rolling_comovement.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved rolling comovement plot to plots/part3_rolling_comovement.png")
    
    # Save report
    with open('data/part3_report.txt', 'w') as f:
        f.write("Table 4: Comovement in Event vs. Placebo Windows\n")
        f.write("-" * 65 + "\n")
        f.write(f"{'Window Type':<20} | {'Vendor A Pairs':<18} | {'Vendor B Pairs (Control)':<22}\n")
        f.write("-" * 65 + "\n")
        f.write(f"{'Event Windows':<20} | {ev_comove_A:<18.6f} | {ev_comove_B:<22.6f}\n")
        f.write(f"{'Placebo Windows':<20} | {pl_comove_A:<18.6f} | {pl_comove_B:<22.6f}\n")
        f.write(f"{'All Other Days':<20} | {oth_comove_A:<18.6f} | {oth_comove_B:<22.6f}\n")
        f.write("-" * 65 + "\n")

if __name__ == "__main__":
    run_part3()
