import matplotlib.pyplot as plt

def display_spectra(wvls, R_f, T_f, R_r, T_r, R = None, T = None, xlims = [210, 2500]):
    
    # Colorscheme
    colors = ["black", "red", "blue"]
    labels = ["forward", "reverse", "with backside"]
    
    fig, axs = plt.subplots(2, sharex=True)
    
    fig.suptitle('R and T spectra')
    axs[0].plot(wvls, R_f, "-", label=labels[0], color=colors[0])
    axs[0].plot(wvls, R_r, "--", label=labels[1], color=colors[1])
    if R is not None:
        axs[0].plot(wvls, R, "-", label=labels[2], color=colors[2])
    axs[0].set_xlim(xlims)
    axs[0].set_ylabel("$R_{fw}$ and $R_{rv}$")

    axs[1].plot(wvls, T_f, "-", label=labels[0], color=colors[0])
    axs[1].plot(wvls, T_r, "--", label=labels[1], color=colors[1])
    if T is not None:
        axs[1].plot(wvls, T, "-", label=labels[2], color=colors[2])
    axs[1].set_xlim(xlims)
    axs[1].set_ylabel("$T_{fw}$ and $T_{rv}$")
    
    axs[1].set_xlabel("Wavelength [nm]")
    axs[1].legend()

    plt.show()