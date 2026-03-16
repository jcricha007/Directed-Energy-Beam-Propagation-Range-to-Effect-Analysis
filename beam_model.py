"""
John C. Richards

Core physics model for a simplified directed energy propagation simulator.

1. Gaussian beam propagation
2. Beer-Lambert atmospheric attenuation
3. Peak and average irradiance
4. Target absorbed power
5. Simple lumped heating estimate
6. Optional radial irradiance profile
7. Optional thermal blooming effect
"""

import numpy as np


def gaussian_beam_with_atmosphere_and_heating(
    wavelength_m,
    w0_m,
    power_w,
    z_m,
    alpha_per_m,
    absorptivity=1.0,
    exposure_s=1.0,
    heated_mass_kg=0.01,
    cp_j_per_kgk=900.0,
    r_m=None,
    include_blooming=False,
    blooming_coeff=0.0
):
    """
    Parameters
    ----------
    wavelength_m : float
        Laser wavelength [m]

    w0_m : float
        Beam waist radius [m]

    power_w : float
        Initial laser power at source [W]

    z_m : float or array-like
        Propagation distance(s) [m]

    alpha_per_m : float
        Atmospheric attenuation coefficient [1/m]

    absorptivity : float, optional
        Fraction of incident power absorbed by the target [0 to 1]

    exposure_s : float, optional
        Exposure time for heating estimate [s]

    heated_mass_kg : float, optional
        Effective heated target mass [kg]

    cp_j_per_kgk : float, optional
        Specific heat capacity of target material [J/(kg*K)]

    r_m : float or array-like, optional
        Radial coordinate(s) for Gaussian intensity profile [m]

    include_blooming : bool, optional
        Turns thermal blooming model on or off

    blooming_coeff : float, optional
        Empirical coefficient controlling how strongly blooming spreads beam

    Returns
    -------
    out : dict
        Dictionary containing model outputs:
            z           : distance array [m]
            zR          : Rayleigh range [m]
            theta       : far-field half-angle divergence [rad]
            w           : beam radius vs distance [m]
            Pz          : beam power vs distance [W]
            I0          : peak irradiance vs distance [W/m^2]
            Iavg        : average irradiance vs distance [W/m^2]
            Pabs        : absorbed target power vs distance [W]
            Qabs        : absorbed energy over exposure time [J]
            deltaT      : simple temperature rise estimate [K]
            P_air_abs   : power absorbed by air [W]
            w_bloom     : blooming contribution to beam radius [m]
            r           : radial coordinate array [m], if provided
            Ir          : radial irradiance profile [W/m^2], if provided
    """
 # %%
    # Input validation
    # To prevent impossible inputs from creating false or illogical answers - simnple booleans
    # ---------------------------------------------------------------------------------------------------
    if wavelength_m <= 0:
        raise ValueError("wavelength_m must be > 0")

    if w0_m <= 0:
        raise ValueError("w0_m must be > 0")

    if power_w < 0:
        raise ValueError("power_w must be >= 0")

    if alpha_per_m < 0:
        raise ValueError("alpha_per_m must be >= 0")

    if not (0.0 <= absorptivity <= 1.0):
        raise ValueError("absorptivity must be between 0 and 1")

    if exposure_s < 0:
        raise ValueError("exposure_s must be >= 0")

    if heated_mass_kg <= 0:
        raise ValueError("heated_mass_kg must be > 0")

    if cp_j_per_kgk <= 0:
        raise ValueError("cp_j_per_kgk must be > 0")

    if blooming_coeff < 0:
        raise ValueError("blooming_coeff must be >= 0")

    # Convert z into a NumPy array for vectorized math
    z = np.atleast_1d(np.array(z_m, dtype=float))

    if np.any(z < 0):
        raise ValueError("All z_m values must be >= 0")

    # Gaussian beam relations

    # Rayleigh range:
        # Distance where the beam radius increase by sqrt2 --> from notes
    zR = np.pi * w0_m**2 / wavelength_m

        # Far-field half-angle divergence (limited diffraction)
    theta = wavelength_m / (np.pi * w0_m)

    # Beam radius v. dist.
        # used to account for diffraction spreading --> notes et all
    w = w0_m * np.sqrt(1.0 + (z / zR)**2)


    # Beer-Lambert atmospheric attenuation:
         # remaining power after going some dist. "z"
    Pz = power_w * np.exp(-alpha_per_m * z)


    # Thermal blooming effect:
        # power absorbed by the air along the beam path
        # this is the energy removed from beam and put into atmosphere
    P_air_abs = power_w - Pz

        # set a default blooming radius term in case blooming is turned off
    w_bloom = np.zeros_like(z)

        # if blooming is enabled, compute added beam spreading due to heated air
    if include_blooming:
        w_bloom = blooming_coeff * np.sqrt(P_air_abs) * z

        # effective beam radius combines Gaussian spreading and blooming spreading
        w = np.sqrt(w**2 + w_bloom**2)


    # Irradiance metrics:
        # Peak irradiance for Gaussian beam
        # energy concentrates towards the center or the beam waist
    I0 = (2.0 * Pz) / (np.pi * w**2)

    # Average irradiance over circular beam area:
        # Guassian beam irradiance avg --> notes etc
    Iavg = Pz / (np.pi * w**2)


    # Target absorption and heating:
        # power absrobned by the target surface/body
    Pabs = absorptivity * Pz

        # energy absorbed over exposure time
    Qabs = Pabs * exposure_s

        # estimated rise in temp using delta-T = Q / m*cp
    deltaT = Qabs / (heated_mass_kg * cp_j_per_kgk)

    # Dictionary creation:
    out = {
        "z": z,
        "zR": zR,
        "theta": theta,
        "w": w,
        "Pz": Pz,
        "I0": I0,
        "Iavg": Iavg,
        "Pabs": Pabs,
        "Qabs": Qabs,
        "deltaT": deltaT,
        "P_air_abs": P_air_abs,
        "w_bloom": w_bloom,
    }

    # Optional radial irradiance profile:
    if r_m is not None:
        r = np.atleast_1d(np.array(r_m, dtype=float))

        if np.any(r < 0):
            raise ValueError("All r_m values must be >= 0")

        # r -> column vector, z-dependent quantities -> row vectors
        r_col = r.reshape(-1, 1)
        w_row = w.reshape(1, -1)
        I0_row = I0.reshape(1, -1)

        # Gaussian radial intensity profile
        Ir = I0_row * np.exp(-2.0 * (r_col**2) / (w_row**2))

        out["r"] = r
        out["Ir"] = Ir

    return out