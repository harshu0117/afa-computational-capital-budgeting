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

def generate_market_data(theta, event_days_A=None, event_sd_factor=5.0, num_days=NUM_DAYS):
    """
    Generates all firm assignments, daily shocks, and returns for a given theta.
    Supports variable sample lengths via num_days (e.g., num_days=4000 for diagnostic testing)
    without PRNG re-seeding between parameter creation and shock generation.
    """
    np.random.seed(SEED)
    
    # 1. Assign vendors (Firms 1-300 Vendor A, 301-500 Vendor B)
    vendors = np.array(['A'] * VENDOR_A_COUNT + ['B'] * VENDOR_B_COUNT)
    
    # 2. Assign usage delta_i ~ U[0, 0.4]
    delta = np.random.uniform(0.0, DELTA_MAX, size=NUM_FIRMS)
    
    # 3. Assign market sensitivity beta_i ~ N(1, 0.3^2)
    beta = np.random.normal(BETA_MEAN, BETA_SD, size=NUM_FIRMS)
    
    # 4. Draw daily shocks for num_days
    m = np.random.normal(0.0, 1.0, size=num_days)
    eta_A = np.random.normal(0.0, 1.0, size=num_days)
    eta_B = np.random.normal(0.0, 1.0, size=num_days)
    epsilon = np.random.normal(0.0, 1.0, size=(num_days, NUM_FIRMS))
    
    # Modify shocks for Part 3 event days if provided
    if event_days_A is not None:
        for d in event_days_A:
            eta_A[d] = eta_A[d] * event_sd_factor
            
    # 5. Build returns
    # Create vendor shock mapping: eta_v of shape (num_days, NUM_FIRMS)
    eta_v = np.zeros((num_days, NUM_FIRMS))
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
