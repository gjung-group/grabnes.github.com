# Input flag reference

GRABNES reads a single input file (`Gendata.in` by convention). Flags are
order-independent, and negative values must be written as `0.0-1.0` instead
of `-1.0`. This page lists the flags encountered in the tutorials; to
discover the full set (and the routines consuming each flag), grep the source
code:

```bash
grep -r "SuperCell ." Src/
```

## Generic

| Flag | Values | Meaning |
|---|---|---|
| `Description` | string | Free-form label for the run. |
| `Prefix` | string | Prefix of all output files (`generate` by convention). |

## Cell building

| Flag | Values | Meaning |
|---|---|---|
| `TypeOfSystem` | `Graphene`, `ReadXYZ`, `TwistedBilayerBasedOnMoireCell`, … | Structure-generating method. |
| `CellSize` | integer | Repetitions of the graphene unit cell (used e.g. to reach a moiré cell size). |
| `Supercell` | integer | Repetitions of the built cell in $x$ and $y$ (Lanczos sampling). |
| `MoireCellParameters` | `i j i' j'` | Hermann indices defining a commensurate moiré cell. |
| `oneLayer` / `twoLayers` | `.true.`/`.false.` | Number of layers for built-in construction. |
| `twoLayersZ1`, `twoLayersZ2` | float (Å) | Approximate $z$ coordinates of bottom/top layers. |
| `Latticepercent` | float | Lattice mismatch, hBN as reference; must equal $-1/\texttt{CellSize}$ for G/hBN effective-model cells. |

## Calculations

| Flag | Values | Meaning |
|---|---|---|
| `Calculate.OnlyDOS` | `.true.`/`.false.` | DOS by Lanczos recursion without time evolution. |
| `Kubo.Calc` | `.true.`/`.false.` | Activate the Lanczos/Kubo parts of the code. |
| `Diag.Calc` | `.true.`/`.false.` | Use exact diagonalization. |
| `Calculate.Bands` | `.true.`/`.false.` | Band structure along `Bands.Path`. |
| `Calculate.DOS` | `.true.`/`.false.` | DOS by diagonalization on a k-grid. |
| `Calculate.spectral` | `.true.`/`.false.` | Spectral function / band unfolding. |

## Neighbors

| Flag | Values | Meaning |
|---|---|---|
| `Neigh.LayerNeighbors` | integer | Neighbor-list capacity per layer; too small gives a segmentation fault. |
| `TB.NeighLevels` | 1–5 | Neighbor levels in the TB model (5 for F2G2). |
| `Neigh.LayerDistFactor` | float | Distance factor for interlayer neighbor detection. |
| `nonBulkSmall` | `.true.`/`.false.` | Less efficient but robust neighbor routine for very small cells. |
| `Bulk`, `BulkSmall` | `.true.`/`.false.` | Bulk (3D-periodic) neighbor treatment. |

## Diagonalization / bands

| Flag | Values | Meaning |
|---|---|---|
| `KGrid` | `nx ny nz` | Monkhorst–Pack grid for diagonalization. |
| `Epsilon` | float (eV) | Energy broadening for the DOS. |
| `NumberofEnergyPoints` | integer | Number of energy points for the DOS. |
| `DOS.Emin`, `DOS.Emax` | float (eV) | Energy window for the diagonalized DOS. |
| `Bands.NumPoints` | integer | k-points per segment of the band path. |
| `&begin Bands.Path n` … `&end Bands.Path` | code block | $n$ high-symmetry points in reduced coordinates. |

## Hamiltonian / TB parameters

| Flag | Values | Meaning |
|---|---|---|
| `TB.OnSiteC` | float (eV) | Carbon onsite energy (F2G2), e.g. 0.4914. |
| `TB.Hopping` | float (eV) | First nearest-neighbor hopping (F2G2), e.g. 3.07504. |
| `TypeOfSL`, `TypeOfBL` | `HTC`, … | Model type: hybrid F2G2 intralayer + TC interlayer. |
| `forceBilayerF2G2Intralayer` | `.true.`/`.false.` | Use bilayer rather than monolayer F2G2 intralayer terms. |
| `addSublatticeMassterm`, `sublatticeMassterm` | `.true.`, float (eV) | Sublattice mass term (gap opening). |
| `KoshinoSR` | `.true.`/`.false.` | Koshino/SHE renormalized interlayer model. |
| `renormalizeCoupling`, `couplingFactor` | `.true.`, float | Renormalize interlayer coupling by $S$ (magic-angle anchoring). |

## Effective G/hBN moiré potential

| Flag | Values | Meaning |
|---|---|---|
| `MoirePotential` | `.true.` | Activate effective-potential routines. |
| `MoireJeil` | `.true.` | Use the Jung 2014 effective potential. |
| `MoireOffDiag` | `.true.`/`.false.` | Include the off-diagonal $H_{AB}$ terms. |
| `MoireOnlyH0`, `MoireOnlyHZ`, `MoireH0AndHZ`, `MoireNoH0AndHZ` | booleans | Select which potential components to include. |
| `MoirePotC0`, `MoirePotCz`, `MoirePotCab` | float (eV) | Amplitudes $C_0, C_z, C_{xy}$ (rigid values: $-0.01013$, $-0.00901$, $0.01134$). |
| `MoirePotPhi0`, `MoirePotPhiz`, `MoirePotPhiab` | float (rad) | Phases $\phi_0, \phi_z, \phi_{xy}$. |

## Lanczos

| Flag | Values | Meaning |
|---|---|---|
| `NumberOfRecursion` | integer | Number of Lanczos recursion steps. |
| `EnergyMin`, `EnergyMax` | float (eV) | Energy window for the recursion DOS. |

## Magnetic field & disorder

| Flag | Values | Meaning |
|---|---|---|
| `MagField` | float (T) | Perpendicular magnetic field. |
| `MagField.Integer` | integer | Field quantum number for the simulation cell. |
| `MagField.InitialInteger`, `MagField.FinalInteger`, `MagField.IntegerStep` | integers | Field scan for Hofstadter/Wannier diagrams. |
| `Anderson`, `AndersonAmp` | `.true.`, float (eV) | On-site Anderson disorder and amplitude $W$. |

## Output

| Flag | Values | Meaning |
|---|---|---|
| `WriteDataFiles` | `.true.`/`.false.` | Write Hamiltonian and auxiliary files (avoid for huge cells). |
| `WritePos` | `.true.`/`.false.` | Write structure files (`generate.pos`, `generate.xyz`). |
