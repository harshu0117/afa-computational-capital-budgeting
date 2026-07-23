import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# Ensure local imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from simulation_core import generate_market_data, THETA_ONE, NUM_FIRMS, NUM_DAYS, VENDOR_A_COUNT
from run_part2 import calculate_residuals

def plot_dual_vendors():
    print("Generating dual-vendor rolling comovement plot...")
    
    # 1. Pick 10 evenly spaced event days for Vendor A
    event_days = np.linspace(50, 950, 10, dtype=int)
    
    # 2. Generate market data with 5x shock factor for Vendor A on event days
    data_event = generate_market_data(THETA_ONE, event_days_A=event_days, event_sd_factor=5.0)
    
    # 3. Calculate residuals
    residuals = calculate_residuals(data_event['r'], data_event['m'])
    
    # 4. Separate Vendor A (0-299) and Vendor B (300-499) residuals
    res_A = residuals[:, :VENDOR_A_COUNT] # (1000, 300)
    res_B = residuals[:, VENDOR_A_COUNT:] # (1000, 200)
    
    # 5. Calculate 11-day rolling correlations
    rolling_comove_A = np.zeros(NUM_DAYS)
    rolling_comove_B = np.zeros(NUM_DAYS)
    
    triu_idx_A = np.triu_indices(VENDOR_A_COUNT, k=1)
    triu_idx_B = np.triu_indices(NUM_FIRMS - VENDOR_A_COUNT, k=1)
    
    for t in range(5, NUM_DAYS - 5):
        # Vendor A window
        window_A = res_A[t-5:t+6, :]
        corr_A = np.corrcoef(window_A, rowvar=False)
        rolling_comove_A[t] = np.mean(corr_A[triu_idx_A])
        
        # Vendor B window
        window_B = res_B[t-5:t+6, :]
        corr_B = np.corrcoef(window_B, rowvar=False)
        rolling_comove_B[t] = np.mean(corr_B[triu_idx_B])
        
    # 6. Plot both lines on the same axes
    plt.figure(figsize=(12, 6))
    days_range = range(5, NUM_DAYS - 5)
    
    plt.plot(days_range, rolling_comove_A[5:NUM_DAYS-5], color='#1f77b4', linewidth=2.0, label='Vendor A Pairs (Shocked Vendor)')
    plt.plot(days_range, rolling_comove_B[5:NUM_DAYS-5], color='#ff7f0e', linewidth=2.0, label='Vendor B Pairs (Control Vendor)')
    
    # Mark event days with red dashed lines
    for idx, ed in enumerate(event_days):
        plt.axvline(x=ed, color='red', linestyle='--', alpha=0.6, label='Vendor A Event Days' if idx == 0 else "")
        
    plt.xlabel('Trading Day (t)', fontsize=12)
    plt.ylabel('Average 11-Day Rolling Residual Correlation', fontsize=12)
    plt.title('Part 3: Rolling Comovement — Vendor A (Shocked) vs. Vendor B (Control)', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11, loc='upper right')
    plt.grid(True, linestyle='--', alpha=0.5)
    
    os.makedirs('plots', exist_ok=True)
    output_path = 'plots/part3_dual_vendors.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Successfully saved graph to {output_path}")

if __name__ == "__main__":
    plot_dual_vendors()
