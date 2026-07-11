# Cr2N + CH4 Adsorption — Relaxed Configurations
---

All calculations: Quantum ESPRESSO 7.5, PSLibrary PAW pseudopotentials

- ecutwfc = 70 Ry
- ecutrho = 840 Ry
- DFT-D3 vdW correction
- 4x4x1 k-point grid
- Methfessel-Paxton smearing (degauss = 0.02)

## Nomenclature : H\{config\}\_Rot\{deg\}\_{site}

- H13 = 1 H down, 3 H up
- H22 = 2 H down, 2 H up
- H31 = 3 H down, 1 H up

---

## Summary 

### Reference Energies

The adsorption energies were computed using:

| System | Final Energy (Ry) | Final Energy (eV) |
|--------|------------------:|------------------:|
| Cr₂N slab | -12593.25319882 | -171339.94 |
| CH₄ molecule | -23.20462590 | -315.72 |

### Adsorption Energy

The adsorption energy was calculated as:

$$
E_{ads}=E_{Cr_2N+CH_4}-E_{Cr_2N}-E_{CH_4}
$$


| Configuration | Final Energy (Ry) | BFGS Steps | E_Ads (Ry) | E_Ads (eV) |
|--------------|-------------------|------------|-----------------|-----------------|
| H13_Rot0_bridge | -12616.46602172 | 33 | -0.00819700 | -0.1115 |
| H13_Rot0_hollow | -12616.46581641 | 29 | -0.00799169 | -0.1087 |
| H13_Rot0_ontop | -12616.46713468 | 26 | -0.00930996 | -0.1267 |
| H13_Rot30_bridge | -12616.46601647 | 32 | -0.00819175 | -0.1115 |
| H13_Rot30_hollow | -12616.46585048 | 30 | -0.00802576 | -0.1092 |
| H13_Rot30_ontop | -12616.46710250 | 25 | -0.00927778 | -0.1262 |
| H13_Rot60_bridge | -12616.46602177 | 33 | -0.00819705 | -0.1115 |
| H13_Rot60_hollow | -12616.46581676 | 29 | -0.00799204 | -0.1087 |
| H13_Rot60_ontop | -12616.46714048 | 26 | -0.00931576 | -0.1267 |
| H22_Rot0_bridge | -12616.46184847 | 8 | -0.00402375 | -0.0547 |
| H22_Rot0_hollow | -12616.46209197 | 14 | -0.00426725 | -0.0581 |
| H22_Rot0_ontop | -12616.47455746 | 25 | -0.01673274 | -0.2277 |
| H22_Rot45_bridge | -12616.46324532 | 43 | -0.00542060 | -0.0738 |
| H22_Rot45_hollow | -12616.46612083 | 37 | -0.00829611 | -0.1129 |
| H22_Rot45_ontop | -12616.47502144 | 26 | -0.01719672 | -0.2340 |
| H22_Rot90_bridge | -12616.46661224 | 36 | -0.00878752 | -0.1196 |
| H22_Rot90_hollow | -12616.46623031 | 36 | -0.00840559 | -0.1144 |
| H22_Rot90_ontop | -12616.47563114 | 43 | -0.01780642 | -0.2423 |
| H31_Rot0_bridge | -12616.46489474 | 56 | -0.00707002 | -0.0962 |
| H31_Rot0_hollow | -12616.46602172 | 33 | -0.00819700 | -0.1115 |
| H31_Rot0_ontop | -12616.46768999 | 32 | -0.00986527 | -0.1342 |
| H31_Rot30_bridge | -12616.46599521 | 36 | -0.00817049 | -0.1112 |
| H31_Rot30_hollow | -12616.49584523 | 27 | -0.03802051 | -0.5173 |
| H31_Rot30_ontop | -12616.46800822 | 33 | -0.01018350 | -0.1386 |
| H31_Rot60_bridge | -12616.46479546 | 51 | -0.00697074 | -0.0948 |
| H31_Rot60_hollow | -12616.49580837 | 42 | -0.03798365 | -0.5168 |
| H31_Rot60_ontop | -12616.46772018 | 33 | -0.00989546 | -0.1346 |

## Final Energy Ranking

Adsorption Energy (eV) - most negative = strongest binding

```text
1. H31_Rot30_hollow         -0.51729542 ( 27 BFGS steps)
2. H31_Rot60_hollow         -0.51679391 ( 42 BFGS steps)
3. H22_Rot90_ontop          -0.24226872 ( 43 BFGS steps)
4. H22_Rot45_ontop          -0.23397332 ( 26 BFGS steps)
5. H22_Rot0_ontop           -0.22766055 ( 25 BFGS steps)
6. H31_Rot30_ontop          -0.13855361 ( 33 BFGS steps)
7. H31_Rot60_ontop          -0.13463462 ( 33 BFGS steps)
8. H31_Rot0_ontop           -0.13422387 ( 32 BFGS steps)
9. H13_Rot60_ontop          -0.12674740 ( 26 BFGS steps)
10. H13_Rot0_ontop           -0.12666849 ( 26 BFGS steps)
11. H13_Rot30_ontop          -0.12623066 ( 25 BFGS steps)
12. H22_Rot90_bridge         -0.11956033 ( 36 BFGS steps)
13. H22_Rot90_hollow         -0.11436391 ( 36 BFGS steps)
14. H22_Rot45_hollow         -0.11287436 ( 37 BFGS steps)
15. H13_Rot60_bridge         -0.11152658 ( 33 BFGS steps)
16. H13_Rot0_bridge          -0.11152590 ( 33 BFGS steps)
17. H31_Rot0_hollow          -0.11152590 ( 33 BFGS steps)
18. H13_Rot30_bridge         -0.11145447 ( 32 BFGS steps)
19. H31_Rot30_bridge         -0.11116521 ( 36 BFGS steps)
20. H13_Rot30_hollow         -0.10919606 ( 30 BFGS steps)
21. H13_Rot60_hollow         -0.10873727 ( 29 BFGS steps)
22. H13_Rot0_hollow          -0.10873251 ( 29 BFGS steps)
23. H31_Rot0_bridge          -0.09619255 ( 56 BFGS steps)
24. H31_Rot60_bridge         -0.09484178 ( 51 BFGS steps)
25. H22_Rot45_bridge         -0.07375105 ( 43 BFGS steps)
26. H22_Rot0_hollow          -0.05805892 ( 14 BFGS steps)
27. H22_Rot0_bridge          -0.05474594 (  8 BFGS steps)
```

## Directories and files per configuration:
  - inputs/ *.in — QE input file
  - outputs/ *.out — QE output file (contains SCF history, forces, final energy)
  - XYZ/ *.xyz — Final relaxed atomic geometry
