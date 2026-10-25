# Bernal bilayer graphene & graphite

```{seealso}
Runnable version in the
[Google Colab notebook](https://colab.research.google.com/drive/12_ofrjJi4pr6U9j-ER1WocYJkqxEffs-?usp=sharing).
```

We revisit the skills learnt in the {doc}`graphene` tutorial by calculating
the electronic band structure of Bernal-stacked bilayer graphene and bulk
graphite. While doing so, we introduce a new method to build the system that
relies on structural information from external files. This can be
particularly useful when reading in relaxed structures from a preliminary
LAMMPS calculation, for instance.

Up to now we only had to provide the code with the `Gendata.in` file, which
contains all the input flags. When using the `ReadXYZ` method, one also has
to provide the `generate.xyz` and `sublatticesSorted.dat` files to inform the
code about the position of the atoms and the sublattice each atom belongs to.
Example files are provided in
[`generate.xyz`](../assets/downloads/generate.xyz) and
[`sublattices.dat`](../assets/downloads/sublattices.dat).

## AB-stacked bilayer graphene

The figure below illustrates Bernal-stacked bilayer graphene, considered the
energetically most stable configuration when stacking two graphene layers on
top of each other. Similarly to the graphene system, this system can be
represented using 4 atoms in the unit cell.

```{task} Task
- Run the input below to obtain the band structure. You might need a lot of
  k-points if you want to capture the fine features close to the K-point.
  Because the system is small, it is still doable in a reasonable amount of
  time.
```

```python
inputStrings_cell = ["TypeOfSystem ReadXYZ",  # read structure from external files
                     "Supercell 1",
                     "CellSize 1",
                     "twoLayers .true.",     # this is a 2-layer system
                     "twoLayersZ1 1.675",    # approx. z coordinate of bottom layer
                     "twoLayersZ2 5.025",    # approx. z coordinate of top layer
                     ]

inputStrings_calc = ["Diag.Calc .true.", "Calculate.Bands .true.", ...]

inputStrings_neigh = ["Neigh.LayerNeighbors 50",
                      "TB.NeighLevels 5",
                      "Neigh.LayerDistFactor 1.2",
                      "nonBulkSmall .true.",
                      ]

inputStrings_diag = ["Bands.NumPoints 50000",
                     "&begin Bands.Path 4",
                     "0.0   0.0  0.0",  # Gamma
                     "0.5   0.0  0.0",  # M
                     "2/3   1/3  0.0",  # K
                     "0.0   0.0  0.0",  # Gamma
                     "&end Bands.Path",
                     ]

inputStrings_ham = ["TB.OnSiteC 0.4914",
                    "TB.Hopping 3.03",
                    "TypeOfSL HTC",
                    # use bilayer F2G2 intralayer terms rather than
                    # the single-layer F2G2 terms
                    "forceBilayerF2G2Intralayer .true.",
                    ]
```

```bash
<GRABNES> Gendata.in > out.log
```

```python
pg.transformBands("generate.bands")
pg.plot_electronic_bandstructure(workingDir, 2, 0.2)
plt.axvline(1.474633, linestyle="dashed", color="grey")
plt.axvline(2.326013, linestyle="dashed", color="grey")
plt.xticks([0.0, 1.474633, 2.326013, 4.028773],
           [r"$\Gamma$", "M", "K", r"$\Gamma$"])
# Uncomment to focus on the fine features at the K-point:
# plt.ylim(-0.1446, -0.1438)
# plt.xlim(2.32601-0.003, 2.32601+0.006)
plt.ylabel("E (eV)")
```

If you correctly ran the calculation, you should see an accurate version of
the electronic band structure of Bernal-stacked bilayer graphene.

```{task} Bonus task
- Change the working directory to calculate the AA-stacked bilayer graphene
  band structure as well. A `generate.xyz` file for the AA stacking is
  provided in the `bilayerGraphene/bandstructureAA` subfolder of the workshop
  materials.
```

## Bulk graphite

It is straightforward to switch from the previous bilayer calculation to bulk
graphite by adjusting the structural input so that interactions between the
bottom of the unit cell and the top of the unit cell are taken into account.

```{task} Task
- Run the input below. Note the differences with the Bernal-stacked bilayer
  calculation.
```

The only changes with respect to the bilayer input are in the neighbor and
path flags — `Bulk .true.` plus `BulkSmall .true.` make the code treat the
cell as a bulk 3D system, and the band path gains the out-of-plane
direction:

```python
inputStrings_neigh = [..., "BulkSmall .true.", "Bulk .true."]

inputStrings_diag = ["Bands.NumPoints 10",
                     "&begin Bands.Path 8",
                     "0.0   0.0  0.0",     # Gamma
                     "1/3   0.0-1/3 0.0",  # K
                     "0.5   0.0   0.0",    # K
                     "0.0   0.0   0.0",    # Gamma
                     "0.0   0.0   0.5",
                     "1/3   0.0-1/3 0.5",
                     "0.5   0.0   0.5",
                     "0.0   0.0   0.5",
                     "&end Bands.Path",
                     ]
```

```python
pg.transformBands("generate.bands")
pg.plot_electronic_bandstructure(workingDir, 2, 0.2)
plt.xticks([0.0, 1.702628, 2.553943, 4.028462,
            4.497357, 6.199985, 7.051300, 8.525820],
           [r"$\Gamma$", "K", "M", r"$\Gamma$", "A", "H", "L", "A"])
plt.ylabel("E (eV)")
```
