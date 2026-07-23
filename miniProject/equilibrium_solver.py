# [Human-Authored]
K_DEFAULT = 0.10
CHI_DEFAULT = 1.0

# [AI-Generated]
import numpy as np

def solve_equilibrium_exact(delta_a, delta_b, k=K_DEFAULT, chi=CHI_DEFAULT):
    """
    Computes exact equilibrium for vendor quality levels delta_a (leader) and delta_b (rival).
    
    Parameters:
      delta_a : float, quality level of vendor A (leader)
      delta_b : float, quality level of vendor B (rival)
      k       : float, crowd charge steepness (default 0.10)
      chi     : float, cost curvature coefficient (default 1.0)
      
    Returns:
      dict containing exact closed-form values:
        - quality_ratio: delta_a / delta_b
        - tipping_threshold: 1 + k / chi
        - m_bar: common net margin
        - D_a, D_b: vendor masses (crowd sizes)
        - delta_tot: total delegation D_a + D_b
        - s_a, s_b: market shares D_v / delta_tot
        - hhi: s_a^2 + s_b^2
        - adoption_risk: 0.2 * (delta_tot)^2
        - concentration_risk: hhi
        - systematic_risk: 0.2 * (delta_tot)^2 * hhi
        - is_tipped: bool, True if rival mass D_b <= 0
    """
    quality_ratio = delta_a / delta_b
    tipping_threshold = 1.0 + k / chi
    
    # 1. Common net margin
    m_bar = (delta_a + delta_b) / (2.0 + k / chi)
    
    # 2. Vendor masses
    D_a = (delta_a - m_bar) / k
    D_b = (delta_b - m_bar) / k
    
    # 3. Check tipping condition
    if D_b <= 0.0:
        is_tipped = True
        D_a = delta_a / (chi + k)
        D_b = 0.0
    else:
        is_tipped = False
        
    # 4. Total delegation & shares
    delta_tot = D_a + D_b
    s_a = D_a / delta_tot
    s_b = D_b / delta_tot
    hhi = s_a**2 + s_b**2
    
    # 5. Systematic risk components
    adoption_risk = 0.2 * (delta_tot**2)
    concentration_risk = hhi
    systematic_risk = adoption_risk * concentration_risk
    
    return {
        'delta_a': delta_a,
        'delta_b': delta_b,
        'quality_ratio': quality_ratio,
        'tipping_threshold': tipping_threshold,
        'm_bar': m_bar,
        'D_a': D_a,
        'D_b': D_b,
        'delta_tot': delta_tot,
        's_a': s_a,
        's_b': s_b,
        'hhi': hhi,
        'adoption_risk': adoption_risk,
        'concentration_risk': concentration_risk,
        'systematic_risk': systematic_risk,
        'is_tipped': is_tipped
    }

def solve_equilibrium_iterative(delta_a, delta_b, k=K_DEFAULT, chi=CHI_DEFAULT, tol=1e-12, max_iter=200):
    """
    Iterative solver for equilibrium share s_a via continuous bisection on s_a in [0, 1].
    Evaluates net firm surplus under simultaneous crowd sizes to verify exact formulas.
    """
    # Test if market tips to A at s_a = 1
    v_a_at_1 = 0.5 * chi * (delta_a / (chi + k))**2
    v_b_at_1 = 0.5 * chi * (delta_b / chi)**2
    
    if v_a_at_1 >= v_b_at_1:
        s_a = 1.0
        D_a = delta_a / (chi + k)
        D_b = 0.0
    else:
        low = 0.5
        high = 1.0
        for _ in range(max_iter):
            mid = 0.5 * (low + high)
            v_a_mid = 0.5 * chi * (delta_a / (chi + k * mid))**2
            v_b_mid = 0.5 * chi * (delta_b / (chi + k * (1.0 - mid)))**2
            diff = v_a_mid - v_b_mid
            if abs(diff) < tol or (high - low) < tol:
                s_a = mid
                break
            if diff > 0:
                low = mid
            else:
                high = mid
        else:
            s_a = 0.5 * (low + high)
            
        D_a = s_a * delta_a / (chi + k * s_a)
        D_b = (1.0 - s_a) * delta_b / (chi + k * (1.0 - s_a))
        
    delta_tot = D_a + D_b
    s_a_res = D_a / delta_tot
    s_b_res = D_b / delta_tot
    hhi = s_a_res**2 + s_b_res**2
    sys_risk = 0.2 * (delta_tot**2) * hhi
    
    return {
        's_a': s_a_res,
        's_b': s_b_res,
        'D_a': D_a,
        'D_b': D_b,
        'delta_tot': delta_tot,
        'hhi': hhi,
        'systematic_risk': sys_risk
    }
