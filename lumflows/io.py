import numpy as np

def to_file(wvls, R_f, T_f, R_r, T_r, R = None, T = None, filename=None):

    if filename is None:
        file = "RTA.txt"

    if R is None and T is None:
        elements_per_row = 5
    else:
        elements_per_row = 7

    with open(file, "w") as f:
        # Loop through the arrays in steps of 7 elements to
        # extract elements for the current row
        for i in range(0, len(wvls), elements_per_row):
            _wavelength = wvls[i:i + elements_per_row]
            _R_f = R_f[i:i + elements_per_row]
            _T_f = T_f[i:i + elements_per_row]
            _R_r = R_r[i:i + elements_per_row]
            _T_r = T_r[i:i + elements_per_row]
            
            # Fill out empty values with zeros if needed
            if R is None:
                _R = np.zeros(elements_per_row)
            else:
                _R = R[i:i + elements_per_row]
            
            if T is None:
                _T = np.zeros(elements_per_row)
            else:
                _T = T[i:i + elements_per_row]

            # Combine the rows into a formatted string
            row = ""
            for j in range(len(_wavelength)):
                row = f"{_wavelength[j].item():.5f}, {_R_f[j].item():.5f}, {_T_f[j].item():.5f}, {_R_r[j].item():.5f}, {_T_r[j].item():.5f}, {_R[j].item():.5f}, {_T[j].item():.5f}\n"
                f.write(row)