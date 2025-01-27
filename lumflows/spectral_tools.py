import math
import numpy as np

def compute_with_backside(wavelength, R_f, T_f, R_r, T_r, N_substrate, d_substrate = 2.0):
    R_b = []
    T_b = []
    R_corr = []
    T_corr = []
    n_air = 1.003                              # air
    d = d_substrate / 1000.0                   # substrate thickness to m
    propagation_angle = 90                     # TODO: check 
    beta = []                                  # absoprtion term

    for i in range(len(wavelength)):
        # Compute R and T for the air-glass interface at the backside of the substrate,
        # using Fresnel eqs (assume normal incidence).
        r_b = (np.abs((np.real(N_substrate[i]) - n_air) / (np.real(N_substrate[i]) + n_air)))**2
        R_b.append(r_b)
        T_b.append(1 - R_b[i])

        # Absorption term
        _alpha = N_substrate[i] * math.sin(math.radians(propagation_angle))        
        _beta = np.imag(((2 * np.pi) / wavelength[i]) * np.sqrt(N_substrate[i]**2 - _alpha**2 * d))
        beta.append(_beta)

    # Backside correction
    for i in range(len(wavelength)):
        
        r_corr = R_f[i] + \
            (T_f[i] * T_r[i] * R_b[i] * math.exp(4 * beta[i])) / (1 - R_r[i] * R_b[i] * math.exp(4 * beta[i]))
        
        t_corr = (T_f[i] * T_b[i] * math.exp(2 * beta[i])) / (1 - R_r[i] * R_b[i] * math.exp(4 * beta[i]))
        
        R_corr.append(r_corr)
        T_corr.append(t_corr)

    return R_corr, T_corr