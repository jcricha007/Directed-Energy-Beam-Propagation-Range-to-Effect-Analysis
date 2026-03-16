"""
John C. Richards

This script compares how different laser power levels affect
peak irradiance over some dist

note:  changing laser power does not alter
beam divergence or beam radius- it only scales the beam energy.

"""

# Numerical library for arrays and vector math
import numpy as np

# Plotting library
import matplotlib.pyplot as plt

# Import the beam propagation model
from beam_model import gaussian_beam_with_atmosphere_and_heating

# Define the propagation distance range

# Distances from 0 to 3000 meters
z = np.linspace(0, 3000, 500)

# Define fixed system parameters

# Laser wavelength [m]
wavelength_m = 1.064e-6

# Beam waist [m]
w0_m = 0.02

# Atmospheric attenuation coefficient [1/m]
alpha_per_m = 2e-4

# Target absorptivity [-]
absorptivity = 0.7

# Exposure time [s]
exposure_s = 2.0

# Effective heated target mass [kg]
heated_mass_kg = 0.01

# Specific heat capacity [J/(kg*K)]
cp_j_per_kgk = 900

# Define laser powers to test
laser_powers_w = [1000, 5000, 10000, 20000]

# Create figure
plt.figure(figsize=(8, 5))

for power_w in laser_powers_w:

    # Call the beam propagation model
    result = gaussian_beam_with_atmosphere_and_heating(
        wavelength_m=wavelength_m,
        w0_m=w0_m,
        power_w=power_w,
        z_m=z,
        alpha_per_m=alpha_per_m,
        absorptivity=absorptivity,
        exposure_s=exposure_s,
        heated_mass_kg=heated_mass_kg,
        cp_j_per_kgk=cp_j_per_kgk
    )

    # Plot peak irradiance vs distance for this power level
    plt.plot(
        z,
        result["I0"],
        label=f"Power = {power_w} W"
    )

# Plot format

plt.title("Peak Irradiance vs Distance for Multiple Laser Powers")
plt.xlabel("Distance, z [m]")
plt.ylabel("Peak Irradiance, I₀ [W/m²]")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.show()