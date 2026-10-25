# Twisted bilayer graphene

```{seealso}
Runnable version in the
[Google Colab notebook](https://colab.research.google.com/drive/12_ofrjJi4pr6U9j-ER1WocYJkqxEffs-?usp=sharing).
```

Twisted bilayer graphene has garnered a lot of attention in recent years due
to the interesting properties it displays. When twisting the two graphene
layers at a specific angle, the hybridization of the two Dirac cones leads to
the formation of a flat band, which can give rise to superconductivity and
Mott insulator signatures. Simulating this requires a commensurate cell —
the theory is summarized in {doc}`../theory/moire-cells`, and the
interlayer model (the SHE model) in {doc}`../theory/models`.

## Building the commensurate cell

Create a twisted bilayer system using the `31 30 30 31` indices and visualize
the structure. The methods below also prepare output files that can be used
as input for a LAMMPS calculation or directly as input for the GRABNES code.
A table with relevant indices is given in
[PRB 106, 115410](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.106.115410).

```python
# Prepare input for the Fortran generator, either from the four integers...
pg.prepare_tBG_commensurate_cell_input([31, 30, 30, 31])
# ...or directly from a target twist angle:
# pg.prepare_tBG_commensurate_cell_input(3.0)
```

```bash
!./a.out   # runs the Fortran generator (template: GenMoire.f90)
```

```python
# Collect the output in different formats, including LAMMPS-compatible files
pg.prepare_tBG_commensurate_cell_xyz()

plt.figure(figsize=(20, 10))
pg.plotStructure("generate.xyz")
plt.gca().set_aspect("equal")
```

You could of course also download the structure and visualize it with VMD or
xCrysDen.

## Hamiltonian

For the tBG Hamiltonian we use the
[SHE model](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.106.115410):
the intralayer part is the F2G2 model already used for single-layer
graphene, and the interlayer terms are a reparametrized, magic-angle
renormalized two-center (TC) model (see {doc}`../theory/models` for the full
expressions).

## Density of states (Lanczos)

```{task} Task
- Calculate the Lanczos DOS and optimize the supercell size to get smooth
  behavior of the curve. The current TB model includes a relatively large
  number of neighbors, so the memory requirements can become quite large. On
  Google Colab resources, consider small cells up to `Supercell 10` for the
  $1.08^\circ$ twist angle.
```

```python
inputStrings_cell = ["TypeOfSystem TwistedBilayerBasedOnMoireCell",
                     "Supercell 10",
                     "MoireCellParameters 31 30 30 31",
                     ]

inputStrings_calc = ["Calculate.OnlyDOS .true.", "Kubo.Calc .true.", ...]

inputStrings_neigh = ["Neigh.LayerNeighbors 100",
                      "TB.NeighLevels 5",
                      "Neigh.LayerDistFactor 4.2",
                      ]

inputStrings_diag = ["Bands.NumPoints 10",
                     "&begin Bands.Path 4",
                     "1/3   0.0-1/3 0.0",  # Gamma
                     "0.0   0.0     0.0",  # M
                     "0.5   0.0     0.0",  # K
                     "1/3   0.0-1/3 0.0",  # Gamma
                     "&end Bands.Path",
                     ]

inputStrings_ham = ["TB.OnSiteC 0.4914",
                    "TB.Hopping 3.5",
                    "TypeOfBL HTC",
                    "renormalizeCoupling .true.",
                    "couplingFactor 1.008",   # S for rigid 3.35 Å structures
                    "KoshinoSR .true.",
                    ]

inputStrings_lanczos = ["EnergyMin 0.0-12.0", "EnergyMax 12.0",
                        "NumberOfRecursion 1000"]
```

```python
pg.plotDOS("generate.DOS")
plt.xlim(0, 1.0)
plt.ylim(0, 0.05)
```

## Electronic band structure and the flat band

Under normal conditions it would not be a problem to calculate the electronic
band structure for the magic-angle system, but on free Google Colab resources
memory and parallelization are too limited. However, since the interlayer
coupling of the SHE model can be renormalized using the $S$ factor, we can
obtain by construction a flat band at a larger twist angle that requires a
much smaller commensurate cell. The estimating formula is

\begin{equation}
\theta_\text{eff} = S \theta_\text{ref}/S^\prime
\end{equation}

where $\theta_\text{ref}$ is the angle of the commensurate cell, with
$S = 0.895$ for structures relaxed with the EXX-RPA-fitted force field and
$S = 1.008$ for rigid structures at $3.35$ Å interlayer distance. Hence for a
rigid system with a twist angle of about $5.08^\circ$, corresponding to
indices `7 6 6 7`, we should use a value of $S^\prime = 4.74$:

```python
Sprime = 1.008 * 5.08 / 1.08   # -> 4.74
```

```{task} Task
- Calculate the electronic band structure and visualize the flat band.
```

```python
inputStrings_cell = ["TypeOfSystem TwistedBilayerBasedOnMoireCell",
                     "Supercell 1",
                     "CellSize 1",
                     "MoireCellParameters 7 6 6 7",
                     ]

inputStrings_calc = ["Diag.Calc .true.", "Calculate.Bands .true.", ...]

inputStrings_ham = ["TB.OnSiteC 0.4914",
                    "TB.Hopping 3.03",
                    "TypeOfBL HTC",
                    "renormalizeCoupling .true.",
                    "couplingFactor 4.7037037",  # S'/S
                    "KoshinoSR .true.",
                    ]
```

```python
pg.transformBands("generate.bands")
pg.plot_electronic_bandstructure(workingDir, 2, 0.2)
plt.ylim(0, 1.5)
```

If you correctly ran the calculation, you should see a flat band occurring
in this $5.08^\circ$ simulation cell when increasing the coupling strength
using the formula above.

```{warning}
This renormalization trick was used for illustration purposes so that flat
bands can be shown on the single-core system Google Colab provides. The
larger the difference between the effective angle and the reference angle,
the less accurate this approach becomes, especially for relaxed systems where
the relaxation strength is angle-dependent. Under normal conditions you would
calculate reference angles very close to the effective angle. This is
realistically doable on most modern clusters in less than 15 minutes for the
first magic angle of tBG.
```

## Reading relaxed structures with `ReadXYZ`

The rigid cells above are a first approximation. To repeat the calculations
with a relaxed structure (e.g. from LAMMPS), switch to
`TypeOfSystem ReadXYZ` and place the relaxed `generate.xyz` together with
`sublatticesSorted.dat` in the working directory.

```{task} Tasks
- Repeat the tBG calculations above using the relaxed structure provided for
  download, and compare the observables with the rigid configuration.
- Bonus: combine this session with the graphene-on-hBN knowledge to simulate
  the same observables for tBG on hBN. Note that exact diagonalization
  requires a commensurate cell; you can avoid this complication by using very
  large supercells with Lanczos, where periodic-boundary effects become
  increasingly negligible.
```

## Exercises from the moiré course notebooks

- Calculate the Lanczos DOS and optimize the supercell size to get clear
  signatures. Because the TB model includes many neighbors, memory
  requirements are much larger than for the 3-neighbor G/hBN effective model;
  `Supercell 5` runs on 128 MB machines, up to `Supercell 20` on large-memory
  machines.
- Compare with the exact-diagonalization DOS. Reminder: the Lanczos DOS is
  renormalized by the number of atoms — multiply it by two times the number
  of atoms and divide by `TB.Hopping` to match the diagonalization DOS; the
  Lanczos energy axis is also in units of `TB.Hopping`.
- Add Anderson disorder (`Anderson .true.`, `AndersonAmp <W>`) and see how
  it affects the DOS.
- Add a magnetic field and compare the DOS with and without disorder. Can you
  explain what you see based on your knowledge of Landau levels?
