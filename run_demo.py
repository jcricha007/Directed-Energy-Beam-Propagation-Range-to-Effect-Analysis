import numpy as np

from beam_model import gaussian_beam_with_atmosphere_and_heating

z = np.linspace(0, 3000, 500)

result_no_bloom = gaussian_beam_with_atmosphere_and_heating(
    wavelength_m=1.064e-6,
    w0_m=0.02,
    power_w=5000,
    z_m=z,
    alpha_per_m=2e-4,
    absorptivity=0.7,
    exposure_s=2.0,
    heated_mass_kg=0.01,
    cp_j_per_kgk=900.0,
    include_blooming=False
)

result_bloom = gaussian_beam_with_atmosphere_and_heating(
    wavelength_m=1.064e-6,
    w0_m=0.02,
    power_w=5000,
    z_m=z,
    alpha_per_m=2e-4,
    absorptivity=0.7,
    exposure_s=2.0,
    heated_mass_kg=0.01,
    cp_j_per_kgk=900.0,
    include_blooming=True,
    blooming_coeff=1e-6
)

print("=== No Blooming ===")
print("Final beam radius:", result_no_bloom["w"][-1])
print("Final peak irradiance:", result_no_bloom["I0"][-1])

print("\n=== With Blooming ===")
print("Final beam radius:", result_bloom["w"][-1])
print("Final peak irradiance:", result_bloom["I0"][-1])
print("Final blooming radius contribution:", result_bloom["w_bloom"][-1])