# 10c: Graphene coherent ARPES map near K+ (Nishi mode)

The zoom of Fig. 8(a) of Zhu, Shi and MacDonald, arXiv:2006.08908: the
constant-energy map at `E = -0.12 eV` in a small window around the valley
`K+ = (4*pi/(3a), 0)`. The Fermi surface is a tiny ring, and its intensity is
*not* uniform along the circumference - it fades and brightens with the
azimuthal angle. That modulation is coherent interference: the photoelectrons
leaving the two atoms of the unit cell travel as one wave, and their
amplitudes add before squaring. The right panel of the figure shows the
bright pixels lying on the interference curve `1 + cos(arg f(k))` of the
two-atom structure factor `f = 1 + exp(i k.a1) + exp(i k.a2)`, between total
darkness and four times a single atom's intensity.

## Expected result

![10c: Graphene coherent ARPES map near K+](reference/graphene_coherent_map.png)

This is the figure `plot.py` draws from the reference data. After `./run.sh`,
`python3 plot.py` writes `reference/graphene_coherent_map.png` from your own
run; the two figures should look the same. The map is drawn on an azimuthal
(hue-rotating) color scale so the modulation along the ring reads as a color
rotation; the intensity values themselves are on the colorbar.

## How to run

```sh
./run.sh          # or GRABNES_BIN=/path/to/grabnes ./run.sh
python3 plot.py
```

The run takes about one second and writes `generate.spectral1A`: every line
holds `kx ky kz E I` for one k point of the grid, each k point repeated once
per energy plane; `plot.py` keeps the plane at the map energy. In Nishi mode
the whole coherent weight is written to sublattice A, so `run.sh` removes the
empty sublattice and layer files.

## Method

- **Nishi mode.** `Spectral.Nishi .true.` (together with
  `Spectral.WeiKu .false.`) selects the coherent single-layer weight of Zhu
  and MacDonald (the route of Nishi's ARPES formula) inside
  `DiagSpectralFunctionKGridInequivalentEnergyCut`: the emission amplitudes
  of all lattice sites are summed with phases `exp(i k.R)` *before* taking
  the modulus square, so the map shows the interference fringes. The Wei-Ku
  weights of `../constant_energy_map/` add the probabilities instead and are
  azimuthally flat for monolayer graphene - that is why this variant exists.
- **Requirement.** Nishi mode needs the `gcell1` initialization fix in
  `lanczosKuboCode/Src/diag.F90` (October 2026): without it the lattice
  vectors entering the interference sum are read uninitialized in
  non-moire runs and the result varies randomly from run to run. With the
  fix the map is exactly reproducible.
- **Energy window.** As in `../constant_energy_map/`, the plane sums the
  states within `Spectral.energyGridResolution = 0.05` eV of `Spectral.Emin`;
  the ring is then about 20 grid points thick and every bright pixel carries
  a value of `1 + cos(arg f(k))` between 0 and 2.

## Files

- `Gendata.in`: the input file.
- `run.sh`: runs GRABNES and removes the sublattice and layer files that a
  single graphene sheet leaves empty.
- `plot.py`: draws `reference/graphene_coherent_map.png` from the run, or
  from `reference/coherent_map.dat` when the run is missing;
  `python3 plot.py --table FILE` writes that table from a finished run.
- `reference/`: the table of the map, `E`, `g0` and the lattice constant in
  its header, and the figure drawn from it.

## See also

- `../constant_energy_map/`, the same map routine with Wei-Ku weights over
  the whole zone (Fig. 8(b) of the paper).
- `../spectral_function_path/`, the spectral function along a k path.
- `../../2006.08908v3.pdf`, the paper behind this figure.
