"""
John C. Richards

Plotting utilities for the Directed Energy Mini Project.

1. Beam radius vs distance
2. Beam power vs distance
3. Irradiance vs distance
4. Temperature rise vs distance

"""

import matplotlib.pyplot as plt


def _apply_plot_style():

    plt.rcParams.update({
        "figure.figsize": (8, 5),
        "axes.grid": True,
        "grid.alpha": 0.3,
        "axes.titlesize": 13,
        "axes.labelsize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "lines.linewidth": 2.0,
        "savefig.dpi": 300,
    })


def plot_beam_radius(z, w, zR=None, save_path=None):
    """
    Plot beam radius vs distance.

    Parameters:

    z : array-like
        Distance along beam path [m]

    w : array-like
        Beam radius [m]

    zR : float, optional
        Rayleigh range [m]

    save_path : str, optional
        Path to save the figure
    """
    _apply_plot_style()

    plt.figure()
    plt.plot(z, w, label="Beam radius")

    if zR is not None:
        plt.axvline(zR, linestyle="--", label=f"Rayleigh range = {zR:.1f} m")

    plt.title("Beam Radius vs Distance")
    plt.xlabel("Distance, z [m]")
    plt.ylabel("Beam radius, w(z) [m]")
    plt.legend()
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")


def plot_power(z, Pz, save_path=None):
    """
    Plot beam power vs distance.

    Parameters
    ----------
    z : array-like
        Distance along beam path [m]

    Pz : array-like
        Beam power [W]

    save_path : str, optional
        Path to save the figure
    """
    _apply_plot_style()

    plt.figure()
    plt.plot(z, Pz, label="Beam power")

    plt.title("Beam Power vs Distance")
    plt.xlabel("Distance, z [m]")
    plt.ylabel("Power, P(z) [W]")
    plt.legend()
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")


def plot_irradiance(z, I0, Iavg=None, save_path=None):
    """
    Plot irradiance vs distance.

    Parameters
    ----------
    z : array-like
        Distance along beam path [m]

    I0 : array-like
        Peak irradiance [W/m^2]

    Iavg : array-like, optional
        Average irradiance [W/m^2]

    save_path : str, optional
        Path to save the figure
    """
    _apply_plot_style()

    plt.figure()
    plt.plot(z, I0, label="Peak irradiance")

    if Iavg is not None:
        plt.plot(z, Iavg, label="Average irradiance")

    plt.title("Irradiance vs Distance")
    plt.xlabel("Distance, z [m]")
    plt.ylabel("Irradiance [W/m²]")
    plt.legend()
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")


def plot_temperature(z, deltaT, save_path=None):
    """
    Plot estimated temperature rise vs distance.

    Parameters
    ----------
    z : array-like
        Distance along beam path [m]

    deltaT : array-like
        Estimated temperature rise [K]

    save_path : str, optional
        Path to save the figure
    """
    _apply_plot_style()

    plt.figure()
    plt.plot(z, deltaT, label="Estimated temperature rise")

    plt.title("Estimated Temperature Rise vs Distance")
    plt.xlabel("Distance, z [m]")
    plt.ylabel("Temperature rise, ΔT [K]")
    plt.legend()
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")


def show_all_plots():
    plt.show()