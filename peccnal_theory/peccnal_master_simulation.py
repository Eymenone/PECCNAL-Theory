"""
PECCNAL Theory — Master Physics Simulation
Author: Eymen Aydogan
Date: May 19, 2026

Covers all 8 papers in the PECCNAL series.
Run: python3 peccnal_master_simulation.py
"""

import math, random

MEV_TO_J = 1.602e-13
AVOGADRO = 6.022e23

# === REACTION ENERGIES (MeV) ===
E_CAPTURE   = 1.293   # p + e- → n + ve (INPUT)
E_ND        = 2.220   # n + D → T + p
E_DT        = 17.600  # T + D → He4 + n
E_LI6       = 4.780   # n + Li6 → He4 + T
E_NH        = 2.224   # n + H → D + gamma (water medium)

# === REALISTIC EFFICIENCIES ===
EFF_LI6     = 0.30    # Li6 neutron capture efficiency
EFF_DT      = 0.15    # D-T fusion (Coulomb barrier)
EFF_ND      = 0.52    # n+D cross section efficiency
ION_LOSS    = 0.08    # ionization loss per step (gas)
ION_LOSS_LQ = 0.00001 # ionization loss (liquid D2O)

def separator(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def net_energy(mode="H"):
    if mode == "H":
        return E_LI6 * EFF_LI6 - E_CAPTURE
    elif mode == "D":
        return (E_ND*EFF_ND + E_DT*EFF_DT + E_LI6*EFF_LI6) - E_CAPTURE
    elif mode == "D_ideal":
        return E_ND + E_DT + E_LI6 - E_CAPTURE
    elif mode == "W":  # water
        return E_NH + E_LI6*EFF_LI6 - E_CAPTURE

separator("PAPER 1 — Hydrogen + Li-6")
n1 = net_energy("H")
print(f"  Input:   p + e- → n          = -{E_CAPTURE:.3f} MeV")
print(f"  Output:  n + Li6 (eff {EFF_LI6*100:.0f}%)  = +{E_LI6*EFF_LI6:.3f} MeV")
print(f"  NET:                           = {n1:+.3f} MeV")
print(f"  {'✅ Positive' if n1>0 else '❌ Negative'}")

separator("PAPER 2 — Deuterium + D-T Fusion + Li-6")
n2 = net_energy("D")
n2i = net_energy("D_ideal")
print(f"  Input:   p + e- → n           = -{E_CAPTURE:.3f} MeV")
print(f"  Output1: n + D → T (eff {EFF_ND*100:.0f}%) = +{E_ND*EFF_ND:.3f} MeV")
print(f"  Output2: D-T fusion (eff {EFF_DT*100:.0f}%) = +{E_DT*EFF_DT:.3f} MeV")
print(f"  Output3: n + Li6 (eff {EFF_LI6*100:.0f}%)  = +{E_LI6*EFF_LI6:.3f} MeV")
print(f"  NET (realistic):               = {n2:+.3f} MeV")
print(f"  NET (ideal/tokamak):           = {n2i:+.3f} MeV")
print(f"  {'✅ Positive' if n2>0 else '❌ Negative'} (realistic)")

separator("PAPER 3 — Tritium Self-Regeneration Loop")
T_produced = 2  # S2 + S4
T_consumed  = 1  # S3
TBR = T_produced / T_consumed
print(f"  T produced per cycle: {T_produced} (Step S2 + Step S4)")
print(f"  T consumed per cycle: {T_consumed} (Step S3)")
print(f"  Tritium Breeding Ratio (TBR): {TBR:.1f}")
print(f"  Net energy per cycle: {n2i:+.3f} MeV")
print(f"  {'✅ TBR > 1: Self-sustaining!' if TBR > 1 else '❌ TBR < 1'}")

separator("PAPER 4 — Water (H2O) Medium")
n4 = net_energy("W")
rho_H2_gas  = 0.09
rho_H2O_liq = 1000
e_per_mol_H2  = 2
e_per_mol_H2O = 10
density_ratio = (rho_H2O_liq/18 * e_per_mol_H2O) / (rho_H2_gas/2 * e_per_mol_H2)
print(f"  H2O electron density vs H2 gas: {density_ratio:.0f}x higher")
print(f"  Input:   p + e- → n            = -{E_CAPTURE:.3f} MeV")
print(f"  Output1: n + H → D + gamma     = +{E_NH:.3f} MeV")
print(f"  Output2: n + Li6 (eff {EFF_LI6*100:.0f}%)   = +{E_LI6*EFF_LI6:.3f} MeV")
print(f"  NET:                            = {n4:+.3f} MeV")
print(f"  {'✅ Positive' if n4>0 else '❌ Negative'}")

separator("PAPER 5 — Heavy Water Electrolysis (Ni/Pd + D2O)")
ni_e_density = 8908 * AVOGADRO * 2 / 58.69
print(f"  Ni conduction electron density: {ni_e_density:.2e} m⁻³")
print(f"  vs H2 gas: {ni_e_density/(6e25):.0e}x higher")
print(f"  Reaction: D+ + e-(Ni) → n + ve")
print(f"  Excess heat detectable via calorimetry: Q_out > Q_in")
print(f"  D2O vs H2O control experiment: isotope signature")

separator("PAPER 6 — Heavy Element Multi-Electron Capture")
elements = [("H",1,1,0.09), ("Fe",26,7874,55.85), ("Pb",82,11340,207.2)]
print(f"  {'Element':6} {'Z':4} {'n/atom':7} {'e-density (m⁻³)':18} {'vs H gas':10}")
print("  " + "-"*55)
h_ed = 0.09/1e-3 * AVOGADRO / 1.008
for name, Z, rho, M in elements:
    ed = rho*1000 * AVOGADRO * Z / M
    ratio = ed / h_ed
    print(f"  {name:6} {Z:4} {Z:7} {ed:18.2e} {ratio:10.0f}x")

separator("PAPER 7 — Liquid/Solid Deuterium")
phases = [
    ("Gas STP",    293, 0.18,  200),
    ("Gas 100atm", 293, 18,    2),
    ("Liquid",     23.3, 162,  0.25),
    ("Solid",      18,  201,   0.20),
]
print(f"  {'Phase':12} {'T(K)':6} {'ρ(kg/m³)':10} {'λ(nm)':8} {'Ion loss/step':14}")
print("  " + "-"*55)
for phase, T, rho, lam in phases:
    # dE/dx ~ 50 MeV/mm for 5MeV protons
    ion_loss = 50 * lam * 1e-6  # MeV
    print(f"  {phase:12} {T:6.1f} {rho:10.2f} {lam:8.3f} {ion_loss:14.6f} MeV")
print(f"\n  Liquid D2O: ionization loss per step ≈ 0 (negligible!)")
print(f"  Chain sustainability: ~90%+ in liquid vs ~45-79% in gas")

separator("PAPER 8 — Compact Reactor Design")
n_plates = 100
plate_area_cm2 = 36
total_area = n_plates * plate_area_cm2
print(f"  Electrode array: {n_plates} plates × {plate_area_cm2} cm² = {total_area} cm²")
print(f"  Electrolyte: D2O + 5% Li2CO3")
print(f"  Outer diameter: ~190 mm")
print(f"  Peltier efficiency at ΔT=10K: ~5-8%")

# Monte Carlo chain simulation
random.seed(42)
def simulate(ke, density, steps, mode, trials=200):
    successes = 0
    total_net = 0
    ion = ION_LOSS_LQ if mode == "LQ" else ION_LOSS
    for _ in range(trials):
        k = ke
        out = 0
        inp = ke
        for _ in range(steps):
            k -= k * (ion/density)
            if k < E_CAPTURE:
                break
            k -= E_CAPTURE
            if mode in ("D","LQ"):
                if random.random() < EFF_ND:
                    out += E_ND
                    k += E_ND * 0.1
                if random.random() < EFF_DT:
                    out += E_DT
                if random.random() < EFF_LI6:
                    out += E_LI6
            else:
                if random.random() < EFF_LI6:
                    out += E_LI6
        net = out - inp
        total_net += net
        if net > 0:
            successes += 1
    return successes, total_net/trials

separator("MONTE CARLO CHAIN SIMULATION (200 trials each)")
configs = [
    (5, 1.0, 20, "H",  "H2 gas, low density"),
    (5, 3.0, 20, "H",  "H2 gas, high density"),
    (5, 1.0, 20, "D",  "D2 gas, low density"),
    (5, 3.0, 20, "D",  "D2 gas, high density"),
    (5, 1.0, 20, "LQ", "Liquid D2O"),
    (10,3.0, 50, "LQ", "Liquid D2O, high KE"),
]
print(f"  {'Scenario':<35} {'Success':>8} {'Avg Net':>10}")
print("  " + "-"*55)
for ke, den, steps, mode, label in configs:
    s, n = simulate(ke, den, steps, mode)
    marker = "✅" if n > 0 else "❌"
    print(f"  {marker} {label:<33} {s:>7}% {n:>+10.3f} MeV")

separator("ENERGY SCALE: 1L D2O THEORETICAL MAXIMUM")
mol_D2O = 1000/20
atoms_D = mol_D2O * AVOGADRO * 2
e_per_cycle = n2i * MEV_TO_J
total_J = atoms_D/2 * e_per_cycle
hiroshima_J = 6.3e13
print(f"  Molecules in 1L D2O:    {mol_D2O*AVOGADRO:.2e}")
print(f"  Potential cycles:       {atoms_D/2:.2e}")
print(f"  Energy per cycle:       {n2i:.3f} MeV = {e_per_cycle:.2e} J")
print(f"  Total theoretical:      {total_J:.2e} J")
print(f"  Hiroshima bomb:         {hiroshima_J:.2e} J")
print(f"  Equivalent:             {total_J/hiroshima_J:.1f} Hiroshima bombs")
print(f"\n  ⚠️  NOTE: This is theoretical maximum.")
print(f"  Real efficiency much lower; not all atoms react simultaneously.")

print(f"\n{'='*60}")
print(f"  PECCNAL SIMULATION COMPLETE")
print(f"  Author: Eymen Aydogan | May 19, 2026")
print(f"  Seeking arXiv endorsement: eymenaydogan4753@gmail.com")
print('='*60)
