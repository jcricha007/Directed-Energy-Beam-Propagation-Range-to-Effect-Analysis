"""
John C. Richards

- compares beam waist tradeoffs under multiple atmospheric
attenuation conditions.

Clearer atmosphere:
    - smaller waists can stay viable longer

Harsher atmosphere:
    - larger waists often become more favorable because they reduce
      divergence and lower blooming susceptibility
"""

import numpy as np
import matplotlib.pyplot as plt

# Import beam propagation model
from beam_model import gaussian_beam_with_atmosphere_and_heating


z = np.linspace(0, 3000, 1000)


wavelength_m = 1.064e-6
power_w = 5000
absorptivity = 0.7
exposure_s = 2.0
heated_mass_kg = 0.01
cp_j_per_kgk = 900.0

include_blooming = True
blooming_coeff = 1e-6

# design / environment cases
beam_waists = [0.005, 0.02, 0.05]          # [m]
alpha_values = [0.0, 1e-4, 5e-4]           # [1/m]


# one figure per atmospheric condition
for alpha_per_m in alpha_values:

    plt.figure(figsize=(8, 5))

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

        plt.plot(
            result["z"],
            result["I0"],
            label=f"w0 = {w0_m:.3f} m"
        )

    plt.title(f"Peak Irradiance vs Distance | alpha = {alpha_per_m:.1e} 1/m")
    plt.xlabel("Distance, z [m]")
    plt.ylabel("Peak Irradiance, I₀ [W/m²]")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

plt.show()