"""
John C. Richards

Figure 1:
    Peak irradiance vs distance for multiple beam waists

Figure 2:
    Peak irradiance vs distance for multiple thermal blooming strengths

Figure 3:
    Effective range design-space heatmap as a function of beam waist and laser power

"""


import os
import csv
import numpy as np
import matplotlib.pyplot as plt

# Import the beam propagation model
from beam_model import gaussian_beam_with_atmosphere_and_heating

# Create output folders

base_output_dir = "outputs"
figures_dir = os.path.join(base_output_dir, "figures")
tables_dir = os.path.join(base_output_dir, "tables")
notes_dir = os.path.join(base_output_dir, "notes")

os.makedirs(figures_dir, exist_ok=True)
os.makedirs(tables_dir, exist_ok=True)
os.makedirs(notes_dir, exist_ok=True)

def compute_range_to_effect(z_vals, irradiance_vals, threshold):
    valid_idx = np.where(irradiance_vals >= threshold)[0]

    if len(valid_idx) == 0:
        return 0.0

    return z_vals[valid_idx[-1]]

wavelength_m = 1.064e-6
alpha_per_m = 2e-4
absorptivity = 0.7
exposure_s = 2.0
heated_mass_kg = 0.01
cp_j_per_kgk = 900.0

# Blooming settings
include_blooming = True
blooming_coeff_default = 1e-6

# Threshold for range-to-effect
irradiance_threshold = 3.0e5

# Figure 1: Beam waist analysis
z = np.linspace(0, 3000, 1000)
beam_waists = [0.005, 0.02, 0.05]
power_w_fig1 = 5000

plt.figure(figsize=(8, 5))

fig1_end_ranges = []

for w0_m in beam_waists:
    result = gaussian_beam_with_atmosphere_and_heating(
        wavelength_m=wavelength_m,
        w0_m=w0_m,
        power_w=power_w_fig1,
        z_m=z,
        alpha_per_m=alpha_per_m,
        absorptivity=absorptivity,
        exposure_s=exposure_s,
        heated_mass_kg=heated_mass_kg,
        cp_j_per_kgk=cp_j_per_kgk,
        include_blooming=include_blooming,
        blooming_coeff=blooming_coeff_default
    )

    plt.plot(
        result["z"],
        result["I0"],
        label=f"w0 = {w0_m:.3f} m"
    )

    range_to_effect = compute_range_to_effect(
        result["z"],
        result["I0"],
        irradiance_threshold
    )
    fig1_end_ranges.append((w0_m, range_to_effect))

plt.title("Figure 1: Peak Irradiance vs Distance for Multiple Beam Waists")
plt.xlabel("Distance, z [m]")
plt.ylabel("Peak Irradiance, I₀ [W/m²]")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "fig1_beam_waist_trade.png"), dpi=300, bbox_inches="tight")

# Figure 2: Thermal blooming analysis
blooming_coeff_values = [0.0, 1e-7, 1e-6, 1e-5]
w0_m_fig2 = 0.02
power_w_fig2 = 5000

plt.figure(figsize=(8, 5))

fig2_end_ranges = []

for blooming_coeff in blooming_coeff_values:

    result = gaussian_beam_with_atmosphere_and_heating(
        wavelength_m=wavelength_m,
        w0_m=w0_m_fig2,
        power_w=power_w_fig2,
        z_m=z,
        alpha_per_m=alpha_per_m,
        absorptivity=absorptivity,
        exposure_s=exposure_s,
        heated_mass_kg=heated_mass_kg,
        cp_j_per_kgk=cp_j_per_kgk,
        include_blooming=True,
        blooming_coeff=blooming_coeff
    )

    if blooming_coeff == 0.0:
        label_text = "No blooming"
    else:
        label_text = f"Blooming coeff = {blooming_coeff:.1e}"

    plt.plot(
        result["z"],
        result["I0"],
        label=label_text
    )

    range_to_effect = compute_range_to_effect(
        result["z"],
        result["I0"],
        irradiance_threshold
    )
    fig2_end_ranges.append((blooming_coeff, range_to_effect))

plt.title("Figure 2: Peak Irradiance vs Distance for Multiple Thermal Blooming Strengths")
plt.xlabel("Distance, z [m]")
plt.ylabel("Peak Irradiance, I₀ [W/m²]")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "fig2_blooming_trade.png"), dpi=300, bbox_inches="tight")

# Figure 3: Design-space heatmap
z_map = np.linspace(0, 10000, 4000)
beam_waists_map = np.linspace(0.005, 0.05, 25)
laser_powers_w = np.linspace(1000, 20000, 25)

range_map = np.zeros((len(laser_powers_w), len(beam_waists_map)))

for i, power_w in enumerate(laser_powers_w):
    for j, w0_m in enumerate(beam_waists_map):

        result = gaussian_beam_with_atmosphere_and_heating(
            wavelength_m=wavelength_m,
            w0_m=w0_m,
            power_w=power_w,
            z_m=z_map,
            alpha_per_m=alpha_per_m,
            absorptivity=absorptivity,
            exposure_s=exposure_s,
            heated_mass_kg=heated_mass_kg,
            cp_j_per_kgk=cp_j_per_kgk,
            include_blooming=True,
            blooming_coeff=blooming_coeff_default
        )

        range_map[i, j] = compute_range_to_effect(
            result["z"],
            result["I0"],
            irradiance_threshold
        )

# Locate global best point in the design map
max_idx = np.unravel_index(np.argmax(range_map), range_map.shape)
best_power = laser_powers_w[max_idx[0]]
best_waist = beam_waists_map[max_idx[1]]
best_range = range_map[max_idx]

plt.figure(figsize=(9, 6))

im = plt.imshow(
    range_map,
    origin="lower",
    aspect="auto",
    extent=[
        beam_waists_map[0], beam_waists_map[-1],
        laser_powers_w[0], laser_powers_w[-1]
    ]
)

plt.colorbar(im, label="Effective Range [m]")
plt.title("Figure 3: Effective Range vs Beam Waist and Laser Power")
plt.xlabel("Beam Waist, w0 [m]")
plt.ylabel("Laser Power [W]")

# Mark the best design point
plt.plot(best_waist, best_power, "wo", markersize=8, markeredgecolor="black")
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "fig3_design_space_map.png"), dpi=300, bbox_inches="tight")

# CSV Expo
summary_csv_path = os.path.join(tables_dir, "summary_metrics.csv")

with open(summary_csv_path, mode="w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow(["Study", "Case", "Value_1", "Value_2", "Value_3"])

    writer.writerow(["Beam Waist Trade", "Power [W]", power_w_fig1, "", ""])
    for w0_m, range_to_effect in fig1_end_ranges:
        writer.writerow(["Beam Waist Trade", f"w0 = {w0_m:.3f} m", "Range-to-effect [m]", range_to_effect, ""])

    writer.writerow(["Thermal Blooming Trade", "Power [W]", power_w_fig2, "", ""])
    for blooming_coeff, range_to_effect in fig2_end_ranges:
        if blooming_coeff == 0.0:
            case_name = "No blooming"
        else:
            case_name = f"Blooming coeff = {blooming_coeff:.1e}"
        writer.writerow(["Thermal Blooming Trade", case_name, "Range-to-effect [m]", range_to_effect, ""])

    writer.writerow(["Design Space Optimum", "Best beam waist [m]", best_waist, "", ""])
    writer.writerow(["Design Space Optimum", "Best power [W]", best_power, "", ""])
    writer.writerow(["Design Space Optimum", "Best effective range [m]", best_range, "", ""])
    writer.writerow(["Design Space Optimum", "Threshold [W/m^2]", irradiance_threshold, "", ""])


# --------------------------------------------------
# Export run summary text file
# --------------------------------------------------

summary_txt_path = os.path.join(notes_dir, "run_summary.txt")

with open(summary_txt_path, mode="w") as f:
    f.write("Directed Energy Mini Project - Final Summary\n")
    f.write("=========================================================\n\n")

    f.write("Fixed Parameters\n")
    f.write("----------------\n")
    f.write(f"Wavelength [m]: {wavelength_m}\n")
    f.write(f"Atmospheric attenuation [1/m]: {alpha_per_m}\n")
    f.write(f"Absorptivity [-]: {absorptivity}\n")
    f.write(f"Exposure time [s]: {exposure_s}\n")
    f.write(f"Heated mass [kg]: {heated_mass_kg}\n")
    f.write(f"Specific heat [J/(kg*K)]: {cp_j_per_kgk}\n")
    f.write(f"Blooming enabled: {include_blooming}\n")
    f.write(f"Default blooming coefficient: {blooming_coeff_default}\n")
    f.write(f"Irradiance threshold [W/m^2]: {irradiance_threshold}\n\n")

    f.write("Beam Waist Trade Results\n")
    f.write("------------------------\n")
    for w0_m, range_to_effect in fig1_end_ranges:
        f.write(f"w0 = {w0_m:.3f} m -> Range-to-effect = {range_to_effect:.2f} m\n")
    f.write("\n")

    f.write("Thermal Blooming Trade Results\n")
    f.write("------------------------------\n")
    for blooming_coeff, range_to_effect in fig2_end_ranges:
        if blooming_coeff == 0.0:
            case_name = "No blooming"
        else:
            case_name = f"Blooming coeff = {blooming_coeff:.1e}"
        f.write(f"{case_name} -> Range-to-effect = {range_to_effect:.2f} m\n")
    f.write("\n")

    f.write("Design Space Best Point\n")
    f.write("-----------------------\n")
    f.write(f"Best beam waist [m]: {best_waist:.5f}\n")
    f.write(f"Best laser power [W]: {best_power:.2f}\n")
    f.write(f"Best effective range [m]: {best_range:.2f}\n\n")

    f.write("Key Interpretation\n")
    f.write("------------------\n")
    f.write("1. An optimal beam waist exists for the chosen atmospheric condition.\n")
    f.write("2. Thermal blooming reduces effective range as beam-medium heating grows.\n")
    f.write("3. Increasing power improves range, but diminishing returns emerge due to propagation losses and blooming.\n")


# --------------------------------------------------
# Print quick terminal summary
# --------------------------------------------------

print("=== Final Trade Study Complete ===")
print(f"Figures saved to: {figures_dir}")
print(f"Summary CSV saved to: {summary_csv_path}")
print(f"Run summary saved to: {summary_txt_path}")
print("")
print(f"Best beam waist [m]: {best_waist:.5f}")
print(f"Best laser power [W]: {best_power:.2f}")
print(f"Best effective range [m]: {best_range:.2f}")


# --------------------------------------------------
# Show all figures
# --------------------------------------------------

plt.show()