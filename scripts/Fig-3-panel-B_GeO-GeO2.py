import os
import json
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.colors as colors
from matplotlib.ticker import AutoMinorLocator


DATA_DIR = "../data/"  # Path to the dGf_summary file (see manuscript for details on how dGf was caluclated)


# Set the matplotlib rcParams to make the plot look better
def set_rc_params():
    """
    Returns:
        dictionary of settings for mpl.rcParams
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
        "figure.figsize": [
            6,
            4,
        ],
    }
    for p in params:
        mpl.rcParams[p] = params[p]
    return params


def read_json(fjson):
    """
    Args:
        fjson (str) - file name of json to read

    Returns:
        dictionary stored in fjson
    """
    with open(fjson) as f:
        return json.load(f)


# Plots the dGf energy landscape from discrete data points
def plot_dGf(
    temperatures,
    pressures,
    dGf,
    cmap="Spectral_r",
    levels=1000,
):

    X, Y = np.meshgrid(
        temperatures, pressures
    )  # Create a meshgrid of temperatures and pressures
    Z = -np.array([dGf["TP"][x] for x in zip(X.flatten(), Y.flatten())]).reshape(
        X.shape
    )  # Create a np array of dGf values which aligns with the meshgrid

    # Shift the colormap to have the center value at 0 for a given level density
    center_value = 0
    vmin, vmax = np.min(Z), np.max(Z)
    levels = np.linspace(vmin, vmax, levels)
    center_index = np.argmin(np.abs(levels - center_value))

    cmap = mpl.colormaps.get_cmap(cmap)
    cmap.set_over(cmap(center_index))
    cmap.set_under(cmap(center_index + 1))

    norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=center_value, vmax=vmax)

    # Convert temperatures from Kelvin to Celsius and pressures from atm to Torr
    temperatures = [t - 273.15 for t in temperatures]
    pressures = [p * 760 for p in pressures]
    X, Y = np.meshgrid(temperatures, pressures)  # redefine meshgrid with new units

    fig, ax = plt.subplots(1, 1, figsize=(10, 8), sharey=True)

    surf1 = ax.contourf(
        X, Y, Z, levels=levels, cmap=cmap, norm=norm
    )  # Create contour plot
    split1 = ax.contour(
        X, Y, Z, levels=[0], colors="black", linewidths=2, linestyles="--"
    )  # Create a contour line at 0 indicating the phase boundary
    ax.scatter(
        600, 5 * 10**-6, marker="*", s=750, color="Black", linewidth=2
    )  # Mark the experimental point

    # Add a colorbar with even ticks
    my_ticks = list(np.linspace(vmin, 0, 4)) + list(np.linspace(0, vmax, 5))
    cbar = fig.colorbar(
        surf1,
        ax=fig.axes,
        ticks=my_ticks,
        format=ticker.FuncFormatter(lambda x, pos: f"{x:.1f}"),
        extend="both",
        label=r"$\Delta G\ (\frac{eV}{atom})$",
    )

    # Axes formatting
    ax.set_yscale("log")
    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel(r"$p_{O_2}$" + r"$\ (Torr)$")
    ax.set_xlim([min(temperatures), max(temperatures)])
    ax.set_ylim([min(pressures), max(pressures)])

    ax.xaxis.set_minor_locator(AutoMinorLocator(4))
    ax.tick_params(
        which="minor",
        axis="both",
        direction="out",
        top=True,
        right=True,
        length=6,
        width=1.5,
    )

    # Save the figure
    plt.savefig(os.path.join("..", "figures", "Panel-B_GeO-GeO2.pdf"))
    plt.close()

    return None


def main():
    set_rc_params()
    summary = read_json(
        os.path.join(DATA_DIR, "dGf_summary.json")
    )  # Load the dGf summary file
    rxn_strings = list(summary.keys())  # Get the reaction strings from the summary file

    # Plot the dGf energy landscape for each reaction (Only GeO + 0.5 * O2 -> GeO2 in this case)
    for rxn_string in rxn_strings:
        temp_press_data = summary[rxn_string]["dGf_TP"].items()

        dGf_dict = {}
        dGf_dict["TP"] = {
            tuple([int(k.split(",")[0]), float(k.split(",")[1])]): v
            for k, v in temp_press_data
        }

        temperatures = sorted(list(set([k[0] for k in dGf_dict["TP"].keys()])))
        pressures = sorted(list(set([k[1] for k in dGf_dict["TP"].keys()])))

        plot_dGf(temperatures, pressures, dGf_dict)

    return None


if __name__ == "__main__":
    main()
