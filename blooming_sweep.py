"""
John C. Richards

- compares how different thermal blooming strengths affect
peak irradiance over distance.

- visualize how added air-heating-induced beam spreading
reduces performance relative to the baseline Gaussian + Beer-Lambert model.

Small blooming coefficient:
    - weak additional spreading
    - mild irradiance loss

Large blooming coefficient:
    - stronger additional spreading
    - faster irradiance collapse
"""

# Numerical library for arrays and vector math
import numpy as np

# Plotting library
import matplotlib.pyplot as plt

# Import the beam propagation model
from beam_model import gaussian_beam_with_atmosphere_and_heating

# Distances from 0 to 3000 meters
z = np.linspace(0, 3000, 500)


# Define fixed laser and target parameters:

# Laser wavelength [m]
wavelength_m = 1.064e-6

# Beam waist [m]
w0_m = 0.02

# Source power [W]
power_w = 5000

# Atmospheric attenuation coefficient [1/m]
alpha_per_m = 2e-4

# Target absorptivity [-]
absorptivity = 0.7

# Exposure time [s]
exposure_s = 2.0

# Effective heated target mass [kg]
heated_mass_kg = 0.01

# Specific heat capacity [J/(kg*K)]
cp_j_per_kgk = 900.0

# Define blooming coefficient cases:

# k_b = 0 --> original no-blooming model
# larger values increase added beam spreading
blooming_coeff_values = [0.0, 1e-7, 1e-6, 1e-5]


plt.figure(figsize=(8, 5))

for blooming_coeff in blooming_coeff_values:

    result = gaussian_beam_with_atmosphere_and_heating(
        wavelength_m=wavelength_m,
        w0_m=w0_m,
        power_w=power_w,
        z_m=z,
        alpha_per_m=alpha_per_m,
        absorptivity=absorptivity,
        exposure_s=exposure_s,
        heated_mass_kg=heated_mass_kg,
        cp_j_per_kgk=cp_j_per_kgk,
        include_blooming=True,
        blooming_coeff=blooming_coeff
    )

    # Label first case clearly as no blooming
    if blooming_coeff == 0.0:
        label_text = "No blooming"
    else:
        label_text = f"Blooming coeff = {blooming_coeff:.1e}"

    # Plot peak irradiance vs distance
    plt.plot(
        z,
        result["I0"],
        label=label_text
    )


# plot format

plt.title("Peak Irradiance vs Distance for Multiple Thermal Blooming Strengths")
plt.xlabel("Distance, z [m]")
plt.ylabel("Peak Irradiance, I₀ [W/m²]")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.show()