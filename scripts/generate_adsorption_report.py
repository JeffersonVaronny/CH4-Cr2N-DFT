#!/usr/bin/env python3

import re
from pathlib import Path

# ==========================================================
# USER PARAMETERS
# ==========================================================

E_SLAB_RY = -12593.25319882      # <-- replace manually
E_CH4_RY  = -23.2046258977     # <-- replace manually

ONLY_PW_CH4 = False  # True = only pw-CH4*.out, False = all *.out

RY_TO_EV = 13.605693009


# ==========================================================
# Locate outputs directory
# ==========================================================


PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = PROJECT_DIR / "results" / "relaxation" / "outputs"
RESULTS_DIR = PROJECT_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)
OUTPUT_MD = RESULTS_DIR / "relaxation" / "README.md"

assert OUTPUTS_DIR.exists(), "No existe .out folder"
print(f"out : { OUTPUTS_DIR}")

if ONLY_PW_CH4:
    out_files = sorted(OUTPUTS_DIR.glob("pw-CH4*.out"))
else:
    out_files = sorted(OUTPUTS_DIR.glob("H*.out"))


print(f"Reading outputs from: {OUTPUTS_DIR}")
print(f"Found {len(out_files)} output files")

results = []

for outfile in out_files:

    text = outfile.read_text(errors="ignore")

    energies = re.findall(
        r'!\s+total energy\s+=\s+([-0-9.]+)\s+Ry',
        text
    )

    if not energies:
        continue

    energy = float(energies[-1])

    bfgs_steps = re.findall(
        r'number of bfgs steps\s+=\s+(\d+)',
        text
    )

    if bfgs_steps:
        bfgs = int(bfgs_steps[-1])
    else:
        bfgs = 0

    name = outfile.stem

    if name.startswith("pw-CH4-"):
        name = name.replace("pw-CH4-", "")

    if name.endswith("_"):
        name = name[:-1]

    e_ads_ry = energy - E_SLAB_RY - E_CH4_RY
    e_ads_ev = e_ads_ry * RY_TO_EV

    results.append(
        {
            "name": name,
            "energy": energy,
            "bfgs": bfgs,
            "eads_ry": e_ads_ry,
            "eads_ev": e_ads_ev,
        }
    )

results.sort(key=lambda x: x["name"])

with open(OUTPUT_MD, "w", encoding="utf-8") as f:

    f.write(
"""# Cr2N + CH4 Adsorption — Relaxed Configurations
---

All calculations: Quantum ESPRESSO 7.5, PSLibrary PAW pseudopotentials

- ecutwfc = 70 Ry
- ecutrho = 840 Ry
- DFT-D3 vdW correction
- 4x4x1 k-point grid
- Methfessel-Paxton smearing (degauss = 0.02)

## Nomenclature : `H{config}_Rot{deg}_{site}`

- H13 = 1 H down, 3 H up
- H22 = 2 H down, 2 H up
- H31 = 3 H down, 1 H up

---

## Summary \n"""
)
    f.write("\n### Reference Energies\n\n")
    f.write("The adsorption energies were computed using:\n\n")

    f.write("| System | Final Energy (Ry) | Final Energy (eV) |\n")
    f.write("|--------|------------------:|------------------:|\n")
    f.write(f"| Cr₂N slab | {E_SLAB_RY:.8f} | {E_SLAB_RY*RY_TO_EV:.2f} |\n")
    f.write(f"| CH₄ molecule | {E_CH4_RY:.8f} | {E_CH4_RY*RY_TO_EV:.2f} |\n\n")

    f.write("### Adsorption Energy\n\n")
    f.write("The adsorption energy was calculated as:\n\n")
    f.write(r"$$")
    f.write("\nE_{ads}=E_{Cr_2N+CH_4}-E_{Cr_2N}-E_{CH_4}\n")
    f.write(r"$$")
    f.write("\n\n")

    f.write("""
| Configuration | Final Energy (Ry) | BFGS Steps | E_Ads (Ry) | E_Ads (eV) |
|--------------|-------------------|------------|-----------------|-----------------|
"""
)

    for r in results:
        f.write(
            f"| {r['name']} | "
            f"{r['energy']:.8f} | "
            f"{r['bfgs']} | "
            f"{r['eads_ry']:.8f} | "
            f"{r['eads_ev']:.4f} |\n"
        )

    f.write("\n")

    f.write(
"""## Final Energy Ranking

Adsorption Energy (eV) - most negative = strongest binding

```text
"""
)
    results.sort(key=lambda x: x["eads_ev"])
    for i, r in enumerate(results, start=1):
        f.write(
            f"{i}. "
            f"{r['name']:<20s} "
            f"{r['eads_ev']:>15.8f} "
            f"({r['bfgs']:>3d} BFGS steps)\n"
        )

    f.write("```\n")

    f.write(
"""
## Directories and files per configuration:
  - inputs/ *.in — QE input file
  - outputs/ *.out — QE output file (contains SCF history, forces, final energy)
  - XYZ/ *.xyz — Final relaxed atomic geometry
""")
print(f"Written {OUTPUT_MD}")