"""
John C. Richards

This script compares how different atmospheric attenuation coefficients
affect peak irradiance over distance

helps visualize how strongly propagation environment
can degrade directed-energy performance.
"""

# Numerical library for array math
import numpy as np

# Plotting library
import matplotlib.pyplot as plt

# Import the beam propagation model
from beam_model import gaussian_beam_with_atmosphere_and_heating

# Define propagation distance range
# Distances from 0 to 3000 m @ 500m step
z = np.linspace(0, 3000, 500)

# Define fixed laser and target parameters

# Laser wavelength [m]
wavelength_m = 1.064e-6

# Beam waist [m]
w0_m = 0.02

# Source power [W]
power_w = 5000

# Target absorptivity [-]
absorptivity = 0.7

# Exposure time [s]
exposure_s = 2.0

# Effective heated mass [kg]
heated_mass_kg = 0.01

# Specific heat capacity [J/(kg*K)]
cp_j_per_kgk = 900

# Define atmospheric attenuation cases
    # Units are 1/m
    # Smaller alpha = clearer atmosphere
    # Larger alpha = more severe atmospheric loss
alpha_values = [0.0, 1e-4, 2e-4, 5e-4]

threshold = 1e6  # W/m^2 irradiance required for effect

effective_ranges = []

for alpha_per_m in alpha_values:

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

    I0 = result["I0"]

    valid = z[I0 >= threshold]

    if len(valid) > 0:
        effective_ranges.append(valid[-1])
    else:
        effective_ranges.append(0)

plt.figure()

plt.plot(alpha_values, effective_ranges, marker='o')

plt.xlabel("Atmospheric Attenuation Coefficient α [1/m]")
plt.ylabel("Effective Engagement Range [m]")
plt.title("Effective Range vs Atmospheric Attenuation")

plt.grid(True)
plt.show()

plt.figure(figsize=(8, 5))

for alpha_per_m in alpha_values:

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

    # Plot peak irradiance vs distance
    plt.plot(
        z,
        result["I0"],
        label=f"alpha = {alpha_per_m:.1e} 1/m"
    )


# plot format

plt.title("Peak Irradiance vs Distance for Multiple Atmospheric Conditions")
plt.xlabel("Distance, z [m]")
plt.ylabel("Peak Irradiance, I₀ [W/m²]")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.show()