from .utils import *

def compute_with_backside(wvls, R_front, T_front, R_front_reverse, T_front_reverse, substrate_name = "B270"):

    # Prepare the substrate optical constants and spectral data (R_backside, T_backside)
    N_substrate = interpolate_substrate_constants(read_mat_file(substrate_name), wvls)
    R_back, T_back = interpolate_substrate_spectral_data(read_spectrum_file(substrate_name), wvls)

    # Compute absoprtion term
    beta = compute_absoprtion_term(wvls, N_substrate)

    # Compute corrected R and T spectra
    R = compute_R_with_backside(wvls, R_front, T_front, R_front_reverse, T_front_reverse, R_back, beta)
    T = compute_T_with_backside(wvls, T_front, R_front_reverse, T_back, R_back, beta)

    return R, T