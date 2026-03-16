"""
John C. Richards

2-D design map showing effective range as a function of:
    1. Beam waist
    2. Laser power

Color represents range-to-effect, defined as the maximum distance at which
peak irradiance stays above a required threshold.

"""

import numpy as np
import matplotlib.pyplot as plt

# Import the beam propagation model
from beam_model import gaussian_beam_with_atmosphere_and_heating

z = np.linspace(0, 10000, 4000)

wavelength_m = 1.064e-6
alpha_per_m = 2e-4
absorptivity = 0.7
exposure_s = 2.0
heated_mass_kg = 0.01
cp_j_per_kgk = 900.0

# Blooming settings
include_blooming = True
blooming_coeff = 1e-6

# Required irradiance threshold for "effect"
irradiance_threshold = 3.0e5

# Define sweep ranges
beam_waists = np.linspace(0.005, 0.05, 25)       # [m]
laser_powers_w = np.linspace(1000, 20000, 25)    # [W]

def compute_range_to_effect(z_vals, irradiance_vals, threshold):
    valid_idx = np.where(irradiance_vals >= threshold)[0]

    if len(valid_idx) == 0:
        return 0.0

    return z_vals[valid_idx[-1]]

# Initialize results map
range_map = np.zeros((len(laser_powers_w), len(beam_waists)))

# Fill range map
for i, power_w in enumerate(laser_powers_w):
    for j, w0_m in enumerate(beam_waists):

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
            include_blooming=include_blooming,
            blooming_coeff=blooming_coeff
        )

        range_map[i, j] = compute_range_to_effect(
            result["z"],
            result["I0"],
            irradiance_threshold
        )

# Plot heatmap
plt.figure(figsize=(9, 6))

im = plt.imshow(
    range_map,
    origin="lower",
    aspect="auto",
    extent=[
        beam_waists[0], beam_waists[-1],
        laser_powers_w[0], laser_powers_w[-1]
    ]
)

plt.colorbar(im, label="Effective Range [m]")

plt.title("Design Space Map: Effective Range vs Beam Waist and Laser Power")
plt.xlabel("Beam Waist, w0 [m]")
plt.ylabel("Laser Power [W]")
plt.tight_layout()
plt.show()