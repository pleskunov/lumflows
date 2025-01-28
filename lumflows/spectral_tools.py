import math
import cmath
import numpy as np

def compute_with_backside(wvls, R_f, T_f, R_r, T_r, N_sub):

    if len(wvls) != len(N_sub):
        raise ValueError("The lengths of wavelengths and refractive index of the substrate must be equal!")

    # Constants
    two_pi: float    = 2.0 * math.pi
    n_air: float     = 1.003
    thickness: float = 1000000.0
    theta: float     = 0.0
    
    R_forward = np.array(R_f, dtype=float).flatten()
    T_forward = np.array(T_f, dtype=float).flatten()
    R_reverse = np.array(R_r, dtype=float).flatten()
    T_reverse = np.array(T_r, dtype=float).flatten()

    # Compute R and T for the air-glass interface at the backside of the substrate, using Fresnel eqs.
    R_back = np.zeros_like(wvls, dtype=float)
    T_back = np.zeros_like(R_back, dtype=float)
    for i in range(len(wvls)):
        n = np.real(N_sub[i])
        R_back[i] = np.abs((n - n_air) / (n + n_air))**2
        T_back[i] = 1.0 - R_back[i]

    # Compute the substrate absoprtion term
    beta_i = np.zeros_like(wvls, dtype=float)
    sin_theta: float = math.sin(math.radians(theta))

    for i in range(len(wvls)):
        # alpha squared
        n_sin_theta: complex = N_sub[i] * sin_theta
        sin2: complex = n_sin_theta * n_sin_theta

        N_square: complex = N_sub[i] * N_sub[i]
        N_s_s: complex = cmath.sqrt(N_square - sin2)

        # Correct branch selection
        if N_s_s.real == 0.0:
            N_s_s = -N_s_s

        beta_i[i] = np.imag(two_pi * thickness * N_s_s / wvls[i])
        
        # Debug
        print(beta_i[i])

    # Compute R and T spectra with backside correction
    R_corrected = np.zeros_like(R_forward, dtype=float)
    T_corrected = np.zeros_like(R_corrected, dtype=float)

    for i in range(len(wvls)):
        R_corrected[i] = R_forward[i] + (T_forward[i] * T_reverse[i] * R_back[i] * math.exp(4.0 * beta_i[i])) / (1.0 - R_reverse[i] * R_back[i] * math.exp(4.0 * beta_i[i]))
        
        T_corrected[i] = (T_forward[i] * T_back[i] * math.exp(2.0 * beta_i[i])) / (1.0 - R_reverse[i] * R_back[i] * math.exp(4.0 * beta_i[i]))

    return R_corrected, T_corrected