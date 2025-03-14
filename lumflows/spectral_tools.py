from .utils import *
from .constants import speed_of_light

def freq_to_wavelength(f):
    return np.array((speed_of_light / f) * 1e9).flatten()

def compute_with_backside(wvls, R_front, T_front, R_front_reverse, T_front_reverse, substrate_name = "B270", N_substrate = None):

    # Prepare the substrate optical constants
    if N_substrate is None:
        N_substrate = interpolate_substrate_constants(read_mat_file(substrate_name), wvls)
    else:
        if len(wvls) != len(N_substrate):
            raise RuntimeError("Lengths of wavelengths and complex index refraction values must be the same.")

        if not np.issubdtype(N_substrate.dtype, np.complexfloating):
            raise TypeError("Refractive index of the substrate must be in the complex form.")
    
    # Compute the substrate spectra (R_backside, T_backside)
    R_back, T_back = compute_substrate_spectra(wvls, N_substrate)

    # Compute absoprtion term
    beta = compute_absoprtion_term(wvls, N_substrate)

    # Compute corrected R and T spectra
    R = compute_R_with_backside(wvls, R_front, T_front, R_front_reverse, T_front_reverse, R_back, beta)
    T = compute_T_with_backside(wvls, T_front, R_front_reverse, T_back, R_back, beta)

    return R, T