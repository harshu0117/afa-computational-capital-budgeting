# [Human-Authored]
NUM_FIRMS = 500
NUM_DAYS = 1000
VENDOR_A_COUNT = 300
VENDOR_B_COUNT = 200
SEED = 42
DELTA_MAX = 0.4
BETA_MEAN = 1.0
BETA_SD = 0.3
THETA_ONE = 0.2
THETA_ZERO = 0.0

# [AI-Generated]
import numpy as np

def generate_market_data(theta, event_days_A=None, event_sd_factor=5.0):
    """
    Generates all firm assignments, daily shocks, and returns for a given theta.
    If event_days_A is provided, vendor A's shock standard deviation is multiplied
    by event_sd_factor on those days.
    """
    np.random.seed(SEED)
    
    # 1. Assign vendors (Firms 1-300 Vendor A, 301-500 Vendor B)
    vendors = np.array(['A'] * VENDOR_A_COUNT + ['B'] * VENDOR_B_COUNT)
    
    # 2. Assign usage delta_i ~ U[0, 0.4]
    delta = np.random.uniform(0.0, DELTA_MAX, size=NUM_FIRMS)
    
    # 3. Assign market sensitivity beta_i ~ N(1, 0.3^2)
    beta = np.random.normal(BETA_MEAN, BETA_SD, size=NUM_FIRMS)
    
    # 4. Draw daily shocks
    m = np.random.normal(0.0, 1.0, size=NUM_DAYS)
    eta_A = np.random.normal(0.0, 1.0, size=NUM_DAYS)
    eta_B = np.random.normal(0.0, 1.0, size=NUM_DAYS)
    epsilon = np.random.normal(0.0, 1.0, size=(NUM_DAYS, NUM_FIRMS))
    
    # Modify shocks for Part 3 event days if provided
    if event_days_A is not None:
        for d in event_days_A:
            # Re-draw or scale vendor A's shock on event days
            # The PDF says: "vendor A's shock is drawn with five times the standard deviation: eta_A,t ~ N(0, 5^2)"
            # Since eta_A is already drawn from N(0,1), we can scale the existing draw by 5
            # to preserve the exact underlying random draw sequence, or re-draw it.
            # Scaling the existing draw is equivalent to drawing from N(0, 5^2) using the same random number.
            eta_A[d] = eta_A[d] * event_sd_factor
            
    # 5. Build returns
    # Create vendor shock mapping: eta_v of shape (NUM_DAYS, NUM_FIRMS)
    eta_v = np.zeros((NUM_DAYS, NUM_FIRMS))
    eta_v[:, :VENDOR_A_COUNT] = eta_A[:, np.newaxis]
    eta_v[:, VENDOR_A_COUNT:] = eta_B[:, np.newaxis]
    
    # Calculate components
    market_part = np.outer(m, beta)
    shared_ai_part = delta * np.sqrt(theta) * eta_v
    firm_luck_coef = np.sqrt(1.0 - (delta ** 2) * theta)
    firm_luck = firm_luck_coef * epsilon
    
    r = market_part + shared_ai_part + firm_luck
    
    return {
        'vendors': vendors,
        'delta': delta,
        'beta': beta,
        'm': m,
        'eta_A': eta_A,
        'eta_B': eta_B,
        'epsilon': epsilon,
        'r': r
    }
