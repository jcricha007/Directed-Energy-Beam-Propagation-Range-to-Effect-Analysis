Directed Energy Propagation Simulator

---------------------------------------------------------------------------------------------

Overview:

This project is a Python-based simulation tool for modeling the propagation of high-energy laser beams through the atmosphere and estimating their effectiveness against a target. 

This sim combines several core physical effects that govern real directed energy systems: 

    - Gaussian beam propagation 
    - Diffraction - limited divergence
    - Atmospheric attenuation via Beer-Lambert Law
    - Thermal Blooming 
    - Target Energy Absorption 
    - Range - to - effect Analysis
    - System trade - space exploration 

My goal was to study and educate myself on how system design parameters( beam waist, power, wavelength) and environmental conditions influence the effective engagement range of the system. 

---------------------------------------------------------------------------------------------

Physics Engine:

This sim models a continuous laser beam propagating through an atmosphere using simplified first order physics principles. 

Gaussian Beam Propagation:

    Beam radius evo is modeled as:
    w(z) = W_o(sqrt(1 + (z/Zr)^2))

    here W_o is beam waist
    Zr is rayleigh range
        Zr = (pi*(W_o)^2) / wavelength

    this describes diffraction - limited spreading of the beam 

Beam Divergence: 

    Far-feild divergence is approximated as:
    theta = wavelength / pi * W_o

    instills that larger beam waist --> smaller divergence & shorter wavelength --> smaller divergence 

Atmospheric Attenuation:

    P(z) = (P_o)exp(-alpha * z)

    here P_o is initial power and alpha is attenuation coeffecient 

    this accounts for absorption and scattering in the atmosphere 

Gaussian Irradiance Distribution:

    Peek Irradiance along beam axis:
    I_o(z) = 2P(z) / (pi * w(z)^2)

    Average Irradiance over the beam cross section:
    I_avg(z) = P(z) / (pi * w(z)^2)

Thermal Blooming Model:

    thermal blooming occurs when the laser heats the medium along its path causing a refractive index gradient that disperses the beam 

    Effective beam waist with blooming accounted for:
    w_eff(z) = sqrt(w(z)^2 + w_bloom(z)^2)

    Blooming Term:
    w_bloom(z) = K_b(sqrt(P_air * z))

    where k_b is the blooming coeff and P_air is the power absorbed by the atmosphere

Target Heating Model:

    Absorbed target power:
    P_abs = A*P(z) --> A is target absorptivity NOT AREA

    Total Absorbed Energy:
    Q = P_abs * t --> t is exposure time in seconds (S)

    Estimated Temperature Rise (Kelvin - Celcius):

    Delta_T = Q / m * C_P
    where m is the heated mass and C_P is the specific heat capacity

Range-to-Effect:

    a ssytem can be c9onsidered effective if the peak irradiance exceeds a requisite threshold
    i.e. I_o(z) >= I_thresh

    the range-to-effect is the maximum distance satisfying this condition

    this metric converts propagation physics into a practical perf measurement 

---------------------------------------------------------------------------------------------

Key Results:

1. Beam - Waist Optimization:
    Very small beam waist provide high intial intensity but suffer from:
        - strong divergence 
        - increased thermal blooming 
    Large waist reduce divergence but decrease intensity 

2. Diminishing Returns with Power:
    Increasing laser power increases range intially but eventually yeilds diminishing returns due to:
        - atmospheric attenuation 
        - thermal blooming 

3. Environmental Sensitivity:
    Atmospheric attenuation strongly influences systems performance while clearer conditions allow:
        -  tighter beams 
        -  longer engagement ranges 

4. Thermal Blooming Limitations:
    High power beams degrade thier own propagation path by heating the fluid around the beam causing diffractiona nd spreading

5. Final Script:
    The final script produces three figures:
        i.) Beam Waist Optimization 
            This figure demonstrates peak irradiance vs distance for multiple beam waist 
            Shows the tradeoff between high initial intesity(small waist) and reduced divergence(large waist)

        ii.) Thermal Blooming Comparison
            This figure demonstrates how beam-induced air heating can degrade long range propagation

        iii.) Design-Space Heatmap
            This figure deomonstrates range as a function of:
                - beam waist 
                - laser power
            Meant to highlight optimal system configuration for the chosen atmospheric conditions 
---------------------------------------------------------------------------------------------
Simulation Outputs:

    this simulation generates several plots:
    - Peak Irradiance v. Distance
    - Thermal Blooming Comparisons 
    - Effective Range Heatmaps 
    - Optimal Beam Waist v. Power
    
    these plots were meant to allow a better visualization between design tradeoffs

---------------------------------------------------------------------------------------------

Sumlation Limits:

    since the sim uses only first order level physical construction it cannot account for:
    - Turbulence Modeling 
    - Apadptive Optics
    - Detailed Radiative Transfer
    - Full Wave Optics Propagation
    - CFD - based Thermal Blooming 

---------------------------------------------------------------------------------------------

Future Iteration Improvements:
    - Wavelength Trade Solutions 
    - Turbulence Modeling 
    - Adaptive Optics Correction
    - Pulsed Laser Modeling 
    - Improved Thermal Blooming Physics i.e. CFD 
    - Atmospheric Condition Libraries

---------------------------------------------------------------------------------------------

Author: John C. Richards | Mechanical and Systems Engineer | NCSU Class of 2026 
Date of this Writing: 3/13/2026

---------------------------------------------------------------------------------------------

*Note: AI was used to debugg and structure this code*
    - thoughts, formulas, workflow, and my understand of this content are sound and my own as is the transparency here 
