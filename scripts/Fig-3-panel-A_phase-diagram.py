import os
import numpy as np
import matplotlib.pyplot as plt

R = 8.6173e-5  # Boltzmann contstant (eV/K)
OMEGA = 0.17  # Interaction parameter (eV/atom)


def find_tangent_touch_points(x, y):

    # Ensure x and y are numpy arrays for numerical operations
    x = np.array(x)
    y = np.array(y)

    # Calculate the derivative using finite differences
    dy = np.diff(y)
    dx = np.diff(x)
    derivatives = dy / dx

    # Find points where the derivative changes sign (crosses zero)
    sign_changes = np.sign(derivatives[:-1]) != np.sign(derivatives[1:])

    # Indices where the tangent line touches the curve
    touch_indices = np.where(sign_changes)[0] + 1  # add 1 to adjust for the diff

    # Return x and y values of these points
    touch_points_x = x[touch_indices]
    touch_points_y = y[touch_indices]

    return touch_points_x, touch_points_y


def find_inflection_points(x, y):

    # Ensure x and y are numpy arrays for numerical operations
    x = np.array(x)
    y = np.array(y)

    # First derivative
    dy = np.diff(y)
    dx = np.diff(x)
    first_derivatives = dy / dx

    # Second derivative
    d2y = np.diff(first_derivatives)
    d2x = np.diff(x[:-1])  # we lose one x value from the first diff
    second_derivatives = d2y / d2x

    # Find points where the second derivative changes sign or is zero
    zero_crossings = np.sign(second_derivatives[:-1]) != np.sign(second_derivatives[1:])
    zero_values = second_derivatives[:-1] == 0

    # Indices where the second derivative is zero
    inflection_indices = (
        np.where(zero_crossings | zero_values)[0] + 1
    )  # adjust index for diff

    # Return x and y values of these points
    inflection_points_x = x[inflection_indices + 1]  # +1 to adjust for the double diff
    inflection_points_y = y[inflection_indices + 1]

    return inflection_points_x, inflection_points_y


def deltaG_mix(x, T):
    return R * T * (x * np.log(x) + (1 - x) * np.log(1 - x)) + OMEGA * x * (1 - x)


def main():

    # Temperature range
    T_range = np.linspace(430, 986.25, 1000)  # Kelvin

    # Define the range of composition
    x = np.linspace(0.00001, 0.99999, 10000)

    binodal = []
    spinodal = []
    for T in T_range:

        G = deltaG_mix(x, T)

        x_bin, y_bin = find_tangent_touch_points(x, G)
        x_bin = [x_bin[0], x_bin[-1]]
        binodal.append((x_bin[0], T))
        binodal.append((x_bin[1], T))

        x_spin, y_spin = find_inflection_points(x, G)
        x_spin = [x_spin[0], x_spin[-1]]
        spinodal.append((x_spin[0], T))
        spinodal.append((x_spin[1], T))

    # Convert binodal and spinodal points to numpy arrays for easier manipulation
    binodal = np.array(binodal)
    spinodal = np.array(spinodal)

    # Sort the binodal and spinodal points by composition
    binodal = binodal[np.argsort(binodal[:, 0])]
    spinodal = spinodal[np.argsort(spinodal[:, 0])]

    # Set figure size here
    plt.figure(figsize=(6, 5))

    # Extract sorted binodal and spinodal points
    x_bin = binodal[:, 0]
    T_bin = binodal[:, 1]
    x_spin = spinodal[:, 0]
    T_spin = spinodal[:, 1]

    # Plot binodal points
    plt.plot(
        x_bin,
        T_bin - 273,
        "-",
        color="darkblue",
        markersize=8,
        markerfacecolor="skyblue",
        label="Binodal",
    )

    # Plot spinodal points
    plt.plot(
        x_spin,
        T_spin - 273,
        "-",
        color="darkred",
        markersize=8,
        markerfacecolor="salmon",
        label="Spinodal",
    )

    # Shade the areas under the curves
    plt.fill_between(x_bin, T_bin - 273, 180, color="skyblue", alpha=0.5)
    plt.fill_between(x_spin, T_spin - 273, 180, color="salmon", alpha=0.5)

    # Shade the areas above the binodal curve (in a neutral color)
    plt.fill_between(
        [0] + list(x_bin) + [1],
        [0] + list(T_bin - 273) + [0],
        800,
        color="lightgrey",
        alpha=0.5,
    )

    # Add grid lines for better readability
    plt.grid(True, linestyle="--", linewidth=0.5)

    # Axis settings
    plt.xticks(font="Arial", fontsize=21)
    plt.yticks(font="Arial", fontsize=21)
    plt.xlabel("$x_{\mathrm{Ge}}$", font="Arial", fontsize=24, labelpad=6)
    plt.ylabel("Temperature (°C)", font="Arial", fontsize=24, labelpad=18)

    # Set the x and y limits
    plt.xlim(0, 1)
    plt.ylim(180, 800)

    # Layout adjustments and save the figure
    plt.tight_layout()
    plt.savefig(os.path.join("..", "figures", "Panel-A_Phase-Diagram.pdf"))
    plt.close()

    return None


if __name__ == "__main__":
    main()
