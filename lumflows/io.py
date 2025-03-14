import numpy as np
import csv
from .utils import num_points

def to_file(wvls, R_f, T_f, R_r, T_r, R = None, T = None, filename=None):

    if filename is None:
        filename = "RTA.txt"

    if R is None and T is None:
        elements_per_row = 5
    else:
        elements_per_row = 7

    with open(filename, "w") as f:
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

def csv2txt(inputf, outputf, headr = 2, interpolate = True, start_x = 250.0, stop_x = 1000.0, step = 1, transpose = True, save_to_file = True):

    buffer = csv(file=inputf + ".csv", header=2)

    if transpose is True:
        buffer = buffer.transpose()

    if interpolate is True:
        number_of_points = num_points(start=start_x, end=stop_x, step=step)
        x = np.linspace(start=start_x, stop=stop_x, num=number_of_points)
        n = np.interp(x=x, xp=buffer[0], fp=buffer[1])
        k = np.interp(x=x, xp=buffer[0], fp=buffer[2])
    else:
        x = buffer[0]
        n = buffer[1]
        k = buffer[2]

    if save_to_file is True:
        output_file = output_file
        with open(output_file, "w") as f:
            f.write("wvls\t n\t k\n")
            for wvl, n_i, k_i in zip(x, n, k):
                f.write(f"{wvl}\t{n_i:.5f}\t{k_i:.5f}\n")

    return x, n, k