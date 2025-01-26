def to_file(wavelength, R_f, T_f, R_r, T_r, R, T, file=None):
    if file is None:
        file = "RTA.txt"

    elements_per_row = 7

    with open(file, "w") as f:
        # Loop through the arrays in steps of 7 elements to
        # extract elements for the current row
        for i in range(0, len(wavelength), elements_per_row):
            _wavelength = wavelength[i:i + elements_per_row]
            _R_f = R_f[i:i + elements_per_row]
            _T_f = T_f[i:i + elements_per_row]
            _R_r = R_r[i:i + elements_per_row]
            _T_r = T_r[i:i + elements_per_row]
            _R = R[i:i + elements_per_row]
            _T = T[i:i + elements_per_row]

            # Combine the rows into a formatted string
            row = ""
            for j in range(len(_wavelength)):
                row = f"{_wavelength[j].item():.5f}, {_R_f[j].item():.5f}, {_T_f[j].item():.5f}, {_R_r[j].item():.5f}, {_T_r[j].item():.5f}, {_R[j].item():.5f}, {_T[j].item():.5f}\n"
                f.write(row)