import os
import numpy as np
from math import pi, sin, radians, exp
from cmath import sqrt

DISPERSION_SUFFIX = "_nk"
#SPECTRAL_DATA_SUFFIX = "_rt" # Deprecated because we calculate R and T at the backside interface ourselves
EXTENSION = ".txt"

def num_points(start: float, end: float, step: float) -> int:    
    return int(np.ceil((end - start) / step)) + 1

def normalize(x):
    return (x - min(x)) / (max(x) - min(x))

def zeros_like(array):
    return np.zeros_like(array, dtype=float)

def _get_root_dir():
    return os.path.dirname(os.path.abspath(__file__))

def _get_mat_file(filename):
    root = _get_root_dir()
    file = os.path.join(root, "db", filename)
    if not os.path.exists(file):
        raise FileNotFoundError(f"File '{filename}' not found in the database!")
    
    return file

def read_mat_file(filename):
    file = _get_mat_file(filename + DISPERSION_SUFFIX + EXTENSION)
    
    return np.loadtxt(file, delimiter="\t", skiprows=1).transpose() # TODO: remove any formatting, must be taken care by user

# Deprecated because we calculate R and T at the backside interface ourselves
#def read_spectrum_file(filename):
#    file = _get_mat_file(filename + SPECTRAL_DATA_SUFFIX + EXTENSION)
#    
#    return np.loadtxt(file).transpose()

def _interpolate(wvls, data, new_wvls):
    return np.interp(new_wvls, wvls, data)

def interpolate_substrate_constants(substrate_constants, new_wvls):

    if substrate_constants.shape[0] > substrate_constants.shape[1]:
        raise RuntimeError("The substrate optical properties array is not properly formatted!")
    else:
        init_wvls, n, k = substrate_constants[0], substrate_constants[1], substrate_constants[2]

    n = _interpolate(init_wvls, n, new_wvls)
    k = _interpolate(init_wvls, k, new_wvls)
    N = n - k * 1j

    return N

# Deprecated because we calculate R and T at the backside interface ourselves
#def interpolate_substrate_spectral_data(substrate_spectra, new_wvls):
#    init_wvls, r, t = substrate_spectra[0], substrate_spectra[1], substrate_spectra[2]
#
#    r = _interpolate(init_wvls, r, new_wvls)
#    t = _interpolate(init_wvls, t, new_wvls)
#
#    return r, t

def _compute_R_backside(N_substrate: complex, n_medium: float = 1.0003):
    # Assume normal incidence
    n_substrate: float = np.real(N_substrate)

    numerator = n_medium - n_substrate
    denominator = n_medium + n_substrate
    R = np.abs(numerator/denominator)

    return R * R

def _compute_T_backside(R_back):
    return 1.0 - R_back

def compute_substrate_spectra(wvls, N_substrate):
    R_back = zeros_like(wvls)
    T_back = zeros_like(R_back)

    for i in range(len(wvls)):
        R_back[i] = _compute_R_backside(N_substrate[i])
        T_back[i] = _compute_T_backside(R_back[i])

    return R_back, T_back

def _compute_beta(wvls, N, theta, thickness):
    two_pi = 2 * pi
    # Compute the substrate absoprtion term
    beta_i = zeros_like(wvls)
    sin_theta: float = sin(radians(theta))

    for i in range(len(wvls)):
        # alpha squared
        n_sin_theta: complex = N[i] * sin_theta
        sin2: complex = n_sin_theta * n_sin_theta
        
        N_square: complex = N[i] * N[i]
        N_s_s: complex = sqrt(N_square - sin2)
    
        # Correct branch selection
        if N_s_s.real == 0.0:
            N_s_s = -N_s_s
    
        beta_i[i] = np.imag(two_pi * thickness * N_s_s / wvls[i])

    return beta_i

def compute_absoprtion_term(wvls, N, theta = 0.0, thickness = 2000000.0):
    return _compute_beta(wvls=wvls, N=N, theta=theta, thickness=thickness)

def _T_with_backside(T_front, R_front_reverse, T_back, R_back, beta):
    return (T_front * T_back * exp(2.0*beta)) / (1.0 - R_front_reverse * R_back * exp(4.0*beta))

def _R_with_backside(R_front, T_front, R_front_reverse, T_front_reverse, R_back, beta):
    return R_front + ((T_front * T_front_reverse * R_back * exp(4.0*beta)) / (1.0 - R_front_reverse * R_back * exp(4.0*beta)))

def compute_T_with_backside(wvls, T_front, R_front_reverse, T_back, R_back, beta):
    T = zeros_like(wvls)

    for i in range(len(wvls)):
        T[i] = _T_with_backside(T_front=T_front[i], R_front_reverse=R_front_reverse[i], T_back=T_back[i], R_back=R_back[i], beta=beta[i])

    return T

def compute_R_with_backside(wvls, R_front, T_front, R_front_reverse, T_front_reverse, R_back, beta):
    R = zeros_like(wvls)

    for i in range(len(wvls)):
        R[i] = _R_with_backside(R_front=R_front[i], T_front=T_front[i], R_front_reverse=R_front_reverse[i], T_front_reverse=T_front_reverse[i], R_back=R_back[i], beta=beta[i])

    return R