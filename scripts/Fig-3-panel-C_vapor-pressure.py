import os
import numpy as np
import matplotlib.pyplot as plt


def activity(x, omega=0.17, kB=8.6173303e-5, T=873.0):
    return x * np.exp(omega * ((1 - x) ** 2) / (kB * T))


def main():
    # Vapor pressure above GeO2 (Torr)
    ref_GeO = 2.29656719364419e-06
    x = np.linspace(0, 1, 1001)
    a = activity(x)
    p_GeOs = 1e6 * a * ref_GeO

    plt.figure(figsize=(5.75, 5))

    # Add light gray shading between x = 0.34 and x = 0.66
    plt.axvspan(0.34, 0.66, color="lightgray", alpha=0.3)

    # Blue line
    plt.plot(x[x <= 0.34], p_GeOs[x <= 0.34], "b-", linewidth=2.75)
    plt.plot(x[x > 0.34], p_GeOs[x > 0.34], "b--", linewidth=2.75)

    # Red line
    plt.plot(
        x[x < 0.66],
        2 * p_GeOs[x < 0.66],
        color="darkred",
        linestyle="--",
        linewidth=2.75,
    )
    plt.plot(
        x[x >= 0.66],
        2 * p_GeOs[x >= 0.66],
        color="darkred",
        linestyle="-",
        linewidth=2.75,
    )

    plt.xlim(0, 1)
    plt.ylim(-0.05, 2 * 2.5)
    plt.xticks(font="Arial", fontsize=21)
    plt.yticks(font="Arial", fontsize=21)
    plt.xlabel("$x_{\mathrm{Ge}}$", fontsize=24, labelpad=6, font="Arial")
    plt.ylabel(
        "$p_{\mathrm{GeO}}$ (10$^{-6}$ Torr)", fontsize=24, labelpad=12, font="Arial"
    )
    plt.tight_layout()
    plt.savefig(os.path.join("..", "figures", "Panel-C_Vapor-Pressure.pdf"))
    plt.close()

    return None


if __name__ == "__main__":
    main()
