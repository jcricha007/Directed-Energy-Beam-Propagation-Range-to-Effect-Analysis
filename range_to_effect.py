"""
John C. Richards

- computes range-to-effect for multiple thermal blooming strengths.

Range-to-effect = the maximum distance at which the beam still delivers
at least a required peak irradiance threshold on target.

"""

# Numerical library for arrays and vector math
import numpy as np

# Plotting library
import matplotlib.pyplot as plt

# Import the beam propagation model
from beam_model import gaussian_beam_with_atmosphere_and_heating

# Distances from 0 to 3000 meters
z = np.linspace(0, 3000, 2000)

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


# Example threshold [W/m^2]
# This is the minimum peak irradiance required for the chosen effect
irradiance_threshold = 3.0e5

# Define blooming coefficient cases
blooming_coeff_values = [0.0, 1e-7, 1e-6, 1e-5]

def compute_range_to_effect(z_vals, irradiance_vals, threshold):
    """
    Returns the maximum distance where irradiance is still >= threshold.
    If threshold is never reached, returns None.
    """
    valid_idx = np.where(irradiance_vals >= threshold)[0]

    if len(valid_idx) == 0:
        return None

    return z_vals[valid_idx[-1]]


plt.figure(figsize=(8, 5))

range_results = []


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

    range_to_effect = compute_range_to_effect(
        result["z"],
        result["I0"],
        irradiance_threshold
    )

    range_results.append((blooming_coeff, range_to_effect))

    if blooming_coeff == 0.0:
        label_text = "No blooming"
    else:
        label_text = f"Blooming coeff = {blooming_coeff:.1e}"

    plt.plot(
        result["z"],
        result["I0"],
        label=label_text
    )

    # Mark the range-to-effect point on the curve
    if range_to_effect is not None:
        idx = np.argmin(np.abs(result["z"] - range_to_effect))
        plt.plot(
            result["z"][idx],
            result["I0"][idx],
            "o"
        )


# --------------------------------------------------
# Plot threshold line
# --------------------------------------------------

plt.axhline(
    irradiance_threshold,
    linestyle="--",
    label=f"Effect threshold = {irradiance_threshold:.2e} W/m²"
)


# --------------------------------------------------
# Format the plot
# --------------------------------------------------

plt.title("Range-to-Effect for Multiple Thermal Blooming Strengths")
plt.xlabel("Distance, z [m]")
plt.ylabel("Peak Irradiance, I₀ [W/m²]")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()


# --------------------------------------------------
# Print range-to-effect results
# --------------------------------------------------

print("=== Range-to-Effect Results ===")
print(f"Irradiance threshold: {irradiance_threshold:.2e} W/m²\n")

for blooming_coeff, range_to_effect in range_results:
    if blooming_coeff == 0.0:
        case_name = "No blooming"
    else:
        case_name = f"Blooming coeff = {blooming_coeff:.1e}"

    if range_to_effect is None:
        print(f"{case_name}: threshold never reached")
    else:
        print(f"{case_name}: max effective range = {range_to_effect:.2f} m")


# --------------------------------------------------
# Show figure
# --------------------------------------------------

plt.show()