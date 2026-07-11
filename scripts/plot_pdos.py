"""
Plot projected DOS for C and nearest Cr atoms for all 6 priority configs.

Usage:
    python plot_pdos.py

Outputs:
    pdos_summary.png  — saved in the same directory as this script

Requirements: numpy, matplotlib, ase
Folder layout expected (all relative to this script):
    xyz/{config}.xyz
    {config}/*.pdos_atm*   (PDOS files from projwfc.x)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from ase.io import read
import glob, os

# Directorio base: carpeta 'scripts'
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Subir un nivel para llegar a 'base'
BASE_DIR   = os.path.abspath(os.path.join(SCRIPT_DIR, os.pardir))

# Directorio 'pos/xyz' dentro de base
XYZ_DIR    = os.path.join(BASE_DIR, "results", "pdos", "xyz")
POS_DIR    = os.path.join(BASE_DIR, "results", "pdos")
RESULTS_DIR = os.path.join(BASE_DIR, 'figures')

CONFIGS = [
    # (folder_name,          Fermi_energy_eV, label)
    ('H31_Rot30_hollow', 5.2880, '−517 meV (chemisorbed)'),
    ('H31_Rot60_hollow', 5.2883, '−517 meV (chemisorbed)'),
    ('H22_Rot90_ontop',  5.2438, '−242 meV (physisorbed)'),
    ('H22_Rot45_ontop',  5.2414, '−234 meV (physisorbed)'),
    ('H22_Rot0_ontop',   5.2412, '−228 meV (physisorbed)'),
    ('H13_Rot0_ontop',   5.1781, '−127 meV (physisorbed)')
    ]

N_NEAREST_CR = 3   # number of nearest Cr atoms to sum over
SMOOTH_WIN   = 7   # moving-average window (points)
EMIN, EMAX   = -12, 6


def load_pdos(path):
    """Load a projwfc.x pdos file → (energy array, DOS summed over m_l)."""
    data = np.loadtxt(path)
    return data[:, 0], data[:, 1:].sum(axis=1)


def find_nearest_cr(atoms, c_idx, n=3):
    """Return 1-based atom indices of the n nearest Cr atoms to atom c_idx."""
    c_pos  = atoms.positions[c_idx]
    cr_idx = [i for i, s in enumerate(atoms.get_chemical_symbols()) if s == 'Cr']
    dists  = sorted((np.linalg.norm(atoms.positions[i] - c_pos), i) for i in cr_idx)
    return [i + 1 for _, i in dists[:n]]


def smooth(y, w):
    return np.convolve(y, np.ones(w) / w, mode='same')


verde_musgo = "#006102"
#blue_color = "#0016F0"
blue_color = "#1D98EF"
gris_oscuro = "#3E3E3E"
fig = plt.figure(figsize=(17, 8))
#fig.patch.set_facecolor(gris_oscuro)
gs  = gridspec.GridSpec(2, 3, hspace=0.4, wspace=0.22)
colors = [ verde_musgo, verde_musgo, blue_color, blue_color, blue_color, blue_color] 
for idx, (name, ef_eV, label) in enumerate(CONFIGS):
    ax  = fig.add_subplot(gs[idx // 3, idx % 3])
    #ax.set_facecolor(gris_oscuro)
    d   = os.path.join(POS_DIR, name)
    xyz = read(os.path.join(XYZ_DIR, f'{name}.xyz'))

    c_idx   = next(i for i, s in enumerate(xyz.get_chemical_symbols()) if s == 'C')
    c_atm   = c_idx + 1
    cr_atms = find_nearest_cr(xyz, c_idx, n=N_NEAREST_CR)

    c_s_tot = c_p_tot = cr_d_tot = None
    for f in glob.glob(f'{d}/pdos_{name}.pdos_atm#{c_atm}(C)_wfc#*(s)'):
        e, dos = load_pdos(f)
        c_s_tot = dos if c_s_tot is None else c_s_tot + dos
    for f in glob.glob(f'{d}/pdos_{name}.pdos_atm#{c_atm}(C)_wfc#*(p)'):
        e, dos = load_pdos(f)
        c_p_tot = dos if c_p_tot is None else c_p_tot + dos
    for cr_a in cr_atms:
        for f in glob.glob(f'{d}/pdos_{name}.pdos_atm#{cr_a}(Cr)_wfc#*(d)'):
            e, dos = load_pdos(f)
            cr_d_tot = dos if cr_d_tot is None else cr_d_tot + dos

    e_ref = e - ef_eV


    if c_s_tot  is not None:
        ax.plot(e_ref, smooth(c_s_tot, SMOOTH_WIN),                   
                color="#1900FF", lw=2, label='C 2s')
    if c_p_tot  is not None:
        ax.plot(e_ref, smooth(c_p_tot, SMOOTH_WIN),                   
                color=blue_color, lw=2, label='C 2p')
    if cr_d_tot is not None:
        ax.plot(e_ref, smooth(cr_d_tot / N_NEAREST_CR, SMOOTH_WIN),   
                color= verde_musgo, lw=2, label='Cr 3d (avg.)')
    # Cambiar color de los bordes de los ejes
    

    # Cambiar color de las etiquetas de los ejes
    #ax.xaxis.label.set_color("white")
    #ax.yaxis.label.set_color("white")

    # Cambiar color del título si quieres que también sea blanco
    #ax.title.set_color("white")
    ax.axvspan(-2, 2,color= verde_musgo, alpha=0.08, zorder=0)
    ax.axvline(0, color="0.45", lw=1.5, ls='--', alpha=0.5)
    ax.set_xlim(EMIN, EMAX)
    ax.set_ylim(bottom=0)
    ax.set_xlabel('E − E$_F$ (eV)', fontsize=11)
    ax.set_ylabel('PDOS (states/eV)', fontsize=11)
    ax.set_title(f'{name.replace("_", " ").replace("0", "0°").replace("5", "5°").replace("Rot", "")}\n{label}', fontsize=15, color=colors[idx])
    ax.set_ylim(0, 12.5)
    ax.legend(fontsize=9.1, loc='upper left')
    ax.tick_params(colors="black", labelsize=10) 

fig.suptitle(
    f'Projected DOS — C and {N_NEAREST_CR} nearest Cr atoms (d-channel averaged)',
    fontsize=17, y=0.98, color= 'black')

out = os.path.join(RESULTS_DIR, 'pdos_summary.png')
fig.savefig(out, dpi=400, bbox_inches='tight')
#plt.show()
plt.close()
print(f'Saved: {out}')
