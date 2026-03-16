"""
John C. Richards

this script is made to do the following: 

- Compare peak irradiance vs distance for multiple beam waist values
- compare how varrying waist values affect laser performance over some dist. 

from notes:
- beam waist, w0, influences two effects:
1. initial peak irradiance 
2. beam divergence 

Remember:

Small Waist - small w0:
    - high initial intensity
    - large divergence
    - poor long-range performance

Large Waist:
    - lower initial intensity 
    - small divergence
    - better long range perf. 

To visualize this --> plot peak irradiance v dist. for array of waist vals. 
"""

import numpy as np
import matplotlib.pyplot as plt

from beam_model import gaussian_beam_with_atmosphere_and_heating

# define the dist. range along beam path 
# Distance array via linspace with 500 sample point over three kilos
z = np.linspace(0, 3000, 500)

# Fixed laser/environment parameters
wavelength_m = 1.064e-6
power_w = 5000
alpha_per_m = 2e-4
absorptivity = 0.7
exposure_s = 2.0
heated_mass_kg = 0.01
cp_j_per_kgk = 900

# Sweep beam waist values to show param sweep 
beam_waists = [0.005, .01, .015, 0.02, .025, .03, .04, 0.05]   # 5 mm, 2 cm, 5 cm
# basic plot def
plt.figure(figsize=(8, 5))

for w0 in beam_waists:
    result = gaussian_beam_with_atmosphere_and_heating(
        wavelength_m=wavelength_m,
        w0_m=w0,
        power_w=power_w,
        z_m=z,
        alpha_per_m=alpha_per_m,
        absorptivity=absorptivity,
        exposure_s=exposure_s,
        heated_mass_kg=heated_mass_kg,
        cp_j_per_kgk=cp_j_per_kgk
    )

    plt.plot(z, result["I0"], label=f"w0 = {w0:.3f} m")

plt.title("Peak Irradiance vs Distance for Multiple Beam Waists")
plt.xlabel("Distance, z [m]")
plt.ylabel("Peak Irradiance, I0 [W/m^2]")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()