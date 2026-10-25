# Welcome to GRABNES's documentation!

This documentation covers everything needed to run GRABNES, from installing
the code to interpreting production results: {doc}`installation` gets you
compiling (or running in the browser via Colab), {doc}`theory/index` explains
the physics — tight-binding models, moiré supercells and observables —
{doc}`examples/index` collects the supported, reproducible example
calculations, {doc}`tutorials/index` walks through the workflows step by
step, and {doc}`user-guide/index` documents the input file and every input
key. Published results are gathered in {doc}`benchmarks/index`, the state of
the code in {doc}`development/index`, and the Fortran units in
{doc}`reference/index`.

```{toctree}
:maxdepth: 2
:caption: Contents

installation
theory/index
examples/index
benchmarks/index
tutorials/index
user-guide/index
development/index
reference/index
```

**GRABNES** (**GRA**phene/**B**N **E**lectronic **S**tructure) is a Fortran
tight-binding package for the electronic structure of layered two-dimensional
materials. The name highlights the two standard materials that can be studied
with this package by layering them into meaningful configurations. Additional
2D materials can be included as well by modifying the code.

Out of the box you can build graphene on hBN, twisted bilayer graphene,
twisted multilayer graphene, hBN-encapsulated single-layer graphene,
encapsulated bilayer graphene, and more, with full control over the twist
angle and the sliding between layers. Commensurate cells are built
automatically to account for periodic boundary conditions.

## What you can compute

::::{grid} 2

:::{grid-item-card} Structures
:link: theory/moire-cells
:link-type: doc

Commensurate moiré supercells with controllable twist angle and interlayer
sliding, for graphene, hBN and their combinations. LAMMPS interface for
structural relaxation.
:::

:::{grid-item-card} Band structures & DOS
:link: theory/observables
:link-type: doc

Electronic band structures and density of states, using Lanczos recursion as
well as exact diagonalization — from a few atoms up to tens of millions.
:::

:::{grid-item-card} Spectral functions
:link: theory/observables
:link-type: doc

Unfolded spectral band structures for direct comparison with ARPES
experiments, local density of states, and probability densities from the
wavefunction distribution.
:::

:::{grid-item-card} Transport & magnetic field
:link: theory/observables
:link-type: doc

Kubo–Greenwood conductivity, Landau levels in a perpendicular magnetic field,
and the effect of Anderson disorder on the DOS.
:::

::::

## Tight-binding models

Several of the tight-binding models used in this code have been developed by
researchers associated with this code. The {doc}`theory/models` page presents
the general approach behind the so-called *hybrid* models, which leverage the
precision of accurate F2G2 models for the intralayer interactions and
reparametrized two-center (TC) models matched as closely as possible to DFT
for the interlayer interactions.

## Getting started

GRABNES is a Fortran code. This can be daunting when you have never used this
language, so to give you the opportunity to get a first taste of the GRABNES
code without worrying about compilation issues and compiler questions, we
have compiled a stable version of the code on Google Colab where you can
interact with it using a Jupyter Notebook with Python as the language of
choice. For heavier use of the capabilities of the code, including its OMP
parallelization capabilities, we recommend compiling the code yourself on your
cluster — see {doc}`installation`.

```{button-link} https://colab.research.google.com/drive/12_ofrjJi4pr6U9j-ER1WocYJkqxEffs-?usp=sharing
:color: primary
:align: center

Open the interactive tutorial in Google Colab
```

## Illustrations

### Magic angle renormalization in twisted bilayer graphene

We can calculate the electronic band structure of twisted bilayer graphene
using our SHE model, an improved two-center (TC) model optimized to capture
the DFT tunneling at the K-point while allowing the user to tune it to capture
the magic angle at a specific value. Here we set $S$ so that the magic angle
occurs at $1.08^\circ$ when using the relaxed structures from an energy
minimization with LAMMPS based on EXX-RPA-informed registry-dependent force
fields. The intralayer terms used in LAMMPS are either the widely used REBO2
force fields or the machine-learning based GAP20 potential.

![Magic angle bands of twisted bilayer graphene](assets/images/tBG.png)

### Twisted multilayer graphene band structures

A wide variety of layered materials can be considered in GRABNES. The
Hamiltonian part of the code supports a 20-layer twisted graphene system,
clearly showing the family of tBG bands expected in such tNG systems. A flag
in the GRABNES input file activates a perpendicular electric field.

![Twisted 20-layer graphene band structure](assets/images/t20G.png)

### Twisted bilayer graphene: band unfolding

Our code calculates band-unfolded band structures that help interpret
experimental ARPES measurements. Here we observe good agreement between
experimental features obtained using nano-ARPES and simulated features
obtained with our package.

![Comparison of experimental ARPES data with simulated band-unfolded data](assets/images/ARPES.png)

Comparison of experimental ARPES data with simulated band-unfolded data using
GRABNES. Figure published in
[Nature Physics](https://www.nature.com/articles/s41567-020-0974-x).

More results are collected in the {doc}`benchmarks/index`.

## Getting in touch

The documentation of the code internals is a work in progress. For specific
questions, open an issue on GitHub or email
[lecontenicolas@gmail.com](mailto:lecontenicolas@gmail.com).
