"""
John C. Richards

This script finds the optimal beam waist for each laser power level

Optimal beam waist = the beam waist that gives the maximum effective range
for a fixed irradiance threshold.

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

beam_waists = np.linspace(0.005, 0.05, 40)       # [m]
laser_powers_w = np.linspace(1000, 20000, 40)    # [W]


def compute_range_to_effect(z_vals, irradiance_vals, threshold):
    valid_idx = np.where(irradiance_vals >= threshold)[0]

    if len(valid_idx) == 0:
        return 0.0

    return z_vals[valid_idx[-1]]

# Find optimal waist for each power
optimal_waists = []
max_ranges = []

for power_w in laser_powers_w:

    best_range = -1.0
    best_waist = None

    for w0_m in beam_waists:

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

        range_to_effect = compute_range_to_effect(
            result["z"],
            result["I0"],
            irradiance_threshold
        )

        if range_to_effect > best_range:
            best_range = range_to_effect
            best_waist = w0_m

    optimal_waists.append(best_waist)
    max_ranges.append(best_range)

# Plot optimal beam waist vs power
plt.figure(figsize=(8, 5))
plt.plot(laser_powers_w, optimal_waists)

plt.title("Optimal Beam Waist vs Laser Power")
plt.xlabel("Laser Power [W]")
plt.ylabel("Optimal Beam Waist, w0 [m]")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

#plot max achievable range vs power
plt.figure(figsize=(8, 5))
plt.plot(laser_powers_w, max_ranges)

plt.title("Maximum Effective Range vs Laser Power")
plt.xlabel("Laser Power [W]")
plt.ylabel("Maximum Effective Range [m]")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# samples print
print("=== Optimal Waist Results ===")
for i in range(0, len(laser_powers_w), 5):
    print(
        f"Power = {laser_powers_w[i]:8.1f} W | "
        f"Optimal w0 = {optimal_waists[i]:.4f} m | "
        f"Max range = {max_ranges[i]:.1f} m"
    )