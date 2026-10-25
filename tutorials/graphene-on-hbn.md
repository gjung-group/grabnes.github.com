# Graphene on h-BN

```{seealso}
Runnable version in the
[Google Colab notebook](https://colab.research.google.com/drive/12_ofrjJi4pr6U9j-ER1WocYJkqxEffs-?usp=sharing).
```

After spending some time with the standard layered combinations of graphene,
we turn our attention to graphene on h-BN. For this session we use an
[effective model extracted from DFT calculations](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.89.205414)
which is accurate close to the K-point. The model collapses the effect of
h-BN in a moiré system by simply modifying the onsite energies and hopping
terms of a reference graphene layer, so the computational cost is reduced by
a factor of two. The Hamiltonian is

$$
H_\text{eff}(\textbf{r})=H_{0}(\textbf{r})+H_{z}(\textbf{r})+H_{xy}(\textbf{r})
$$

based on the local stacking function
$\textbf{d}(\textbf{r}) = (\alpha \mathcal{R}(\theta)-1)\textbf{r}$ where
$\alpha = a_G/a_{BN} = 1+\epsilon$ and $\mathcal{R}(\theta)$ is the rotation
operator acting on an atom at lattice site $\textbf{r}$. See
{doc}`../theory/models` for the full expressions of $H_0$, $H_z$ and $H_{xy}$.

## Input file and parameters

The following flags add the effective moiré model on top of a pristine
graphene system.

```python
inputStrings_cell = ["TypeOfSystem Graphene",
                     "Supercell 1",
                     "CellSize 55",  # moiré cell size; see Latticepercent below
                     ]

inputStrings_calc = ["Calculate.OnlyDOS .false.", "Kubo.Calc .false.",
                     "Diag.Calc .false.", "Calculate.Bands .false.",
                     "Calculate.DOS .false.", "Calculate.spectral .false.",
                     ]

inputStrings_ham = ["TB.OnSiteC 0.0",
                    "TB.Hopping 3.03",
                    "MoirePotential .true.",  # activate the effective potential
                    "MoireJeil .true.",       # use the Jung 2014 potential
                    "MoireOffDiag .true.",    # include the off-diagonal H_AB terms
                    "MoireOnlyH0 .true.",     # include only H0
                    "MoireOnlyHZ .false.",
                    "MoireNoH0AndHZ .false.",
                    "MoireH0AndHZ .false.",   # include both H0 and Hz
                    "MoirePotC0    0-0.01013",        # parameters for the
                    "MoirePotCz    0-0.00901",        # rigid configuration
                    "MoirePotCab    0.01134",         #
                    "MoirePotPhi0   1.510233401750693",  #
                    "MoirePotPhiz   0.147131255943122",  #
                    "MoirePotPhiab  0.342084533390889",  #
                    # lattice mismatch, hBN taken as reference (hence the
                    # negative sign). Must equal -1/CellSize; adjust CellSize
                    # accordingly for different moiré cell sizes.
                    "Latticepercent  0-0.018181818181818",
                    "WriteDataFiles .true.",
                    "WritePos .true.",
                    ]
```

```{note}
`Latticepercent` must be set to $-1/\texttt{CellSize}$. For `CellSize 55`
this gives $-1/55 = -0.01818\ldots$, which is why the value above works for a
$55\times55$ system. The sign is negative because the hBN layer is taken as
the reference.
```

## Visualizing the Hamiltonian

Because the effective model modifies the onsite energies of the graphene
layer depending on the local displacement between a carbon atom and the
virtual B and N atoms, the effect can be visualized directly with a scatter
plot of the energies. The `WriteDataFiles .true.` flag writes the Hamiltonian
files (among others); avoid it for very large systems such as the big
supercells used for Lanczos calculations.

```python
pg.plot_onsite_energies("generate.pos", "generate.e")
plt.title(r"onsite energies from $H_0$")
```

As a visual check on the implementation, compare this real-space
representation of the $H_0$-induced onsite energies with the corresponding
displacement-dependent maps in
[Jung, PRB 89, 205414 (2014)](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.89.205414).

## Density of states

```python
inputStrings_calc = ["Calculate.OnlyDOS .true.", "Kubo.Calc .true.", ...]

inputStrings_cell = ["TypeOfSystem Graphene", "Supercell 10", "CellSize 55"]

inputStrings_neigh = ["Neigh.LayerNeighbors 5", "TB.NeighLevels 1"]

inputStrings_lanczos = ["EnergyMin 0.0-1.0", "EnergyMax 1.0",
                        "NumberOfRecursion 1000"]
```

Use `"MoireH0AndHZ .true."` and `"MoireOnlyH0 .false."` to include both $H_0$
and $H_z$ in this DOS calculation.

```python
pg.plotDOS("generate.DOS")
plt.xlim(-0.2, 0.2)
plt.ylim(0.0, 0.04)
```

```{task} Exercises
- The value of `Latticepercent` above works for a $55\times55$ system. Why?
  Modify it for a $56\times56$ system. Why the negative sign?
- Plot the onsite energy of each atom as a scatter plot whose color encodes
  the energy, and confirm that the resulting moiré pattern is periodic.
- Calculate the DOS for a single moiré unit cell using Lanczos recursion and
  plot `generate.DOS`. Why does the plot look spiky?
- Run a convergence study of this DOS by increasing the `Supercell` value.
- Calculate the DOS using exact diagonalization.
- Calculate the electronic band structure of this system.
- Add a magnetic field and repeat the previous steps. Why can't you use exact
  diagonalization? Hint: read up on the Peierls phase substitution, see for
  instance [A. Cresti, Phys. Rev. B 103, 045402 (2021)](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.103.045402).
```

## Magnetic field DOS

### Without disorder

The magnetic field is controlled either by the integer that relates the flux
quantum to the simulation cell size, or directly in Tesla.

```python
inputStrings_mag = ["MagField.Integer 100",  # integer controlling the field
                    # "MagField 50",         # or specify the field in Tesla
                    # "MagField.InitialInteger 0",  # scan the field to build
                    # "MagField.FinalInteger 1000", # Hofstadter or Wannier
                    # "MagField.IntegerStep 2",     # diagrams
                    ]
```

```python
pg.plotDOS("generate.DOS")
plt.xlim(-0.6, 0.6)
plt.ylim(0.0, 0.08)
```

### Anderson disorder

To illustrate the modular nature of the code when building the Hamiltonian,
here is what happens when adding Anderson disorder on top of the G/hBN
effective model in the presence of a magnetic field:

```python
inputStrings_disorder = ["Anderson .true.",
                         "AndersonAmp 1.0",
                         ]
```

```python
pg.plotDOS("generate.DOS")
plt.xlim(-0.6, 0.6)
plt.ylim(0.0, 0.08)
```

If you ran the code correctly, the Landau levels become wider due to the
presence of more localized disorder states in the tails around the center of
the Landau level where the extended states reside. If the disorder is
increased even further, the Landau levels cannot form anymore and a regular
Anderson disorder insulator develops at all energies, where all the states
are localized.
