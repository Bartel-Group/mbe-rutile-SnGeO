import os
import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

OMEGA = 0.1765  # Interaction parameter (eV/atom)
KB = 8.6173303e-5  # Boltzmann constant (eV/K)
T_EXP = 873.0  # Experimental temperature (K)


def set_rc_params():
    """
    Sets the Matplotlib rc parameters to match the desired style.
    """
    params = {
        "axes.linewidth": 2,
        "axes.unicode_minus": False,
        "figure.dpi": 300,
        "font.size": 26,
        "font.family": "arial",
        "legend.frameon": False,
        "legend.handletextpad": 0.4,
        "legend.handlelength": 1,
        "legend.fontsize": 22,
        "mathtext.default": "regular",
        "savefig.bbox": "tight",
        "xtick.labelsize": 26,
        "ytick.labelsize": 26,
        "xtick.major.size": 8,
        "ytick.major.size": 8,
        "xtick.major.width": 2,
        "ytick.major.width": 2,
        "xtick.top": True,
        "ytick.right": True,
        "axes.edgecolor": "black",
        "figure.figsize": [8, 6],
    }
    for p in params:
        mpl.rcParams[p] = params[p]
    return params


def pad_array(arr, length, pad_value=np.nan):
    """
    Pad an array to a specified length with a given pad value.
    """
    return np.pad(arr, (0, length - len(arr)), "constant", constant_values=pad_value)


def activity(x, omega=OMEGA, kB=KB, T=T_EXP):
    return x * math.exp(omega * ((1 - x) ** 2) / (kB * T))


def map_interval(value, src_min, src_max, dst_min=0, dst_max=1):
    ratio = (value - src_min) / (src_max - src_min)
    mapped_value = dst_min + ratio * (dst_max - dst_min)
    return mapped_value


def introduce_breaks(x, y, max_jump):
    x_new = []
    y_new = []
    for i in range(1, len(y)):
        if abs(y[i] - y[i - 1]) > max_jump:
            x_new.append(np.nan)
            y_new.append(np.nan)
        x_new.append(x[i])
        y_new.append(y[i])
    return np.array(x_new), np.array(y_new)


def calculate_eq_content(p_GeOs, p_Sn_0, x, Ge_rich_press, Ge_lim, sticking_coeff=1.0):
    p_Sn_0 *= sticking_coeff

    eq_Ge_content = []
    Ge_flux = []
    two_ph_Ge_content = []
    two_ph_Ge_flux = []
    for p_Ge_0 in np.linspace(5e-7, 3.8e-6, 400):
        p_Ge_0 *= sticking_coeff

        plausible_eqns = []
        plausible_x = []
        for xv, p_GeO in zip(x, p_GeOs):
            if p_GeO < p_Ge_0:
                plausible_eqns.append(
                    ((p_Ge_0 - p_GeO) / (p_Ge_0 - p_GeO + p_Sn_0)) - xv
                )
                plausible_x.append(xv)

        if min(plausible_eqns) < 0 and max(plausible_eqns) > 0:
            plausible_eqns = [abs(v) for v in plausible_eqns]
            ind = np.argmin(plausible_eqns)
            if (plausible_x[ind] <= Ge_lim) or (plausible_x[ind] >= (1 - Ge_lim)):
                eq_Ge_content.append(plausible_x[ind])
                Ge_flux.append(p_Ge_0)
            else:
                if p_Ge_0 > Ge_rich_press:
                    eq_Ge_content.append(1 - Ge_lim)
                    Ge_flux.append(p_Ge_0)
                    two_ph_Ge_content.append(Ge_lim)
                    two_ph_Ge_flux.append(p_Ge_0)
                else:
                    eq_Ge_content.append(Ge_lim)
                    Ge_flux.append(p_Ge_0)

    Ge_flux = np.array(Ge_flux)
    two_ph_Ge_flux = np.array(two_ph_Ge_flux)

    max_jump = 0.1

    Ge_flux_broken, eq_Ge_content_broken = introduce_breaks(
        Ge_flux, eq_Ge_content, max_jump
    )
    two_ph_Ge_flux_broken, two_ph_Ge_content_broken = introduce_breaks(
        two_ph_Ge_flux, two_ph_Ge_content, max_jump
    )

    return Ge_flux_broken, eq_Ge_content_broken


def main():

    # Set the rcParams
    set_rc_params()

    ref_GeO = 2.29656719364419e-06  # Vapor pressure above GeO2 (Torr)
    Ge_lim = 0.34  # Ge (metastable) solubility limit

    Ge_rich_press = activity(1 - Ge_lim) * 2 * ref_GeO
    Sn_rich_press = activity(Ge_lim) * ref_GeO

    x = np.linspace(0, 0.99, 10001)
    a = [activity(xv) for xv in x]

    p_GeOs = []
    for xv, av in zip(x, a):
        if xv <= Ge_lim:
            p_GeOs.append(av * ref_GeO)
        elif xv <= (1 - Ge_lim):
            Ge_rich_coeff = map_interval(xv, src_min=Ge_lim, src_max=1 - Ge_lim)
            Sn_rich_coeff = 1 - Ge_rich_coeff
            press = Ge_rich_coeff * Ge_rich_press + Sn_rich_coeff * Sn_rich_press
            p_GeOs.append(press)
        else:
            p_GeOs.append(av * 2 * ref_GeO)

    # Define a range of p_Sn_0 values
    p_Sn_0_values = np.linspace(5e-7, 3.8e-6, 400)
    Ge_flux_values = []
    eq_Ge_content_values = []

    # Compute eq_Ge_content_broken for each p_Sn_0 and find the maximum length
    max_length = 0
    for p_Sn_0 in p_Sn_0_values:
        Ge_flux_broken, eq_Ge_content_broken = calculate_eq_content(
            p_GeOs, p_Sn_0, x, Ge_rich_press, Ge_lim
        )
        Ge_flux_values.append(Ge_flux_broken)
        eq_Ge_content_values.append(eq_Ge_content_broken)
        if len(Ge_flux_broken) > max_length:
            max_length = len(Ge_flux_broken)

    # Pad all arrays to the maximum length
    Ge_flux_values = np.array([pad_array(arr, max_length) for arr in Ge_flux_values])
    eq_Ge_content_values = np.array(
        [pad_array(arr, max_length) for arr in eq_Ge_content_values]
    )

    # Filter out NaN values for extent calculation
    valid_ge_flux = Ge_flux_values[~np.isnan(Ge_flux_values)]
    valid_eq_ge_content = eq_Ge_content_values[~np.isnan(eq_Ge_content_values)]

    # Plot the heatmap with the new formatting
    plt.figure(figsize=(10, 8))
    plt.imshow(
        eq_Ge_content_values,
        aspect="auto",
        origin="lower",
        extent=[
            valid_ge_flux.min() * 1e6,
            valid_ge_flux.max() * 1e6,
            p_Sn_0_values.min() * 1e6,
            p_Sn_0_values.max() * 1e6,
        ],
        cmap="viridis",
    )
    plt.colorbar(label="$x_{\mathrm{Ge}}$")

    plt.xlabel("$\it{p}_{\mathrm{Ge}}$ (10$^{-6}$ Torr)", labelpad=10)
    plt.ylabel("$\it{p}_{\mathrm{Sn}}$ (10$^{-6}$ Torr)", labelpad=16)

    plt.tick_params(axis="both", which="major")
    plt.gca().xaxis.set_minor_locator(mpl.ticker.AutoMinorLocator(4))
    plt.gca().tick_params(
        which="minor", axis="both", direction="out", length=6, width=1.5
    )

    plt.tight_layout()
    plt.savefig(os.path.join("..", "figures", "Panel-D_Composition-Heatmap.pdf"))
    plt.show()
    plt.close()

    return None


if __name__ == "__main__":
    main()
