import matplotlib.pyplot as plt

def display_rta(wavelength, R_f, T_f, R_r, T_r, R_corr, T_corr, xlims = [250, 2500]):
    
    colors = ["black", "#4361ee", "#e5383b"]
    
    fig, axs = plt.subplots(2, sharex=True)
    
    fig.suptitle('R, T and A')
    axs[0].plot(wavelength, R_f, "-", label="forward", color=colors[0])
    axs[0].plot(wavelength, R_r, "--", label="reverse", color=colors[1])
    axs[0].plot(wavelength, R_corr, "-", label="corrected", color=colors[2])
    axs[0].set_xlim(xlims)
    axs[0].set_ylabel("$R_{f}$ and $R_{r}$")

    axs[1].plot(wavelength, T_f, "-", label="forward", color=colors[0])
    axs[1].plot(wavelength, T_r, "--", label="backward", color=colors[1])
    axs[1].plot(wavelength, T_corr, "-", label="corrected", color=colors[2])
    axs[1].set_xlim(xlims)
    axs[1].set_ylabel("$T_{f}$ and $T_{r}$")
    
    axs[1].set_xlabel("Wavelength (nm)")
    axs[1].legend()

    plt.show()