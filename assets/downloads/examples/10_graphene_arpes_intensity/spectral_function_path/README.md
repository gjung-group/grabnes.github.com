# 10a: Pristine graphene ARPES spectral function along a k path

The photoemission intensity `I(k,E)` of one graphene sheet along the
`K-Gamma-M-K'` line of the Brillouin zone, the same path as in example 01,
computed with the spectral function on a k grid instead of the density of
states: the Dirac cone with its linear crossing at `K` and `E = 0`, the saddle
points (van Hove singularities) at `E = +-g0 = +-3.1 eV` near `M`, and the
`sigma` bands that reach `+-3*g0 = +-9.3 eV` at `Gamma` inside the window of
`+-10.5 eV`.

The intensity is the squared modulus of the Bloch amplitudes on the two
sublattices with the photoemission matrix element of Wei and Ku,
Phys. Rev. B 95, 085420 (2017), and a Gaussian of width `Kubo.Epsilon` in
place of the default energy bin, so the result is deterministic and takes half
a second.

## Expected result

![10: Pristine graphene ARPES spectral function](reference/graphene_arpes.png)

This is the figure `plot.py` draws from the reference data. After `./run.sh`,
`python3 plot.py` writes `reference/graphene_arpes.png` from your own run;
the two figures should look the same.

## Run

```sh
./run.sh
python3 plot.py
```

The calculation writes `generate.spectral1A` and `generate.spectral1B` and
`job.out`; the plotting step writes `reference/graphene_arpes.png`. If the
calculation has not been run, `plot.py` uses `reference/spectral_map.dat`,
the same two columns collected in one table.

## Method

- **System.** `Run.TypeOfSystem Graphene` with one neighbor level and
  `TB.Hopping 3.1`, so `g0 = 3.1 eV` and the Fermi level of the half-filled
  band sits at `E = 0`.
- **Spectral function.** `Calculate.Spectral .true.` selects the k-grid
  spectral function, `Spectral.WeiKu .true.` the matrix element of Wei and Ku
  (without it the weights stay zero), and
  `Spectral.UseGaussianBroadening .true.` replaces the energy bin of
  `Spectral.energyGridResolution` by a Gaussian of width `Kubo.Epsilon`
  (in units of `g0`).
- **Path.** `Spectral.Path` gives the high-symmetry points in reciprocal
  coordinates of the lattice cell, here the same `K-Gamma-M-K'` path as in
  example 01; `Spectral.NumPoints` is the number of k points per segment of
  the first path line, here 20 for `K-Gamma` and proportionally more or fewer
  for the other segments.
- **Energy window.** `Spectral.Emin` and `Spectral.Emax` are in units of
  `g0`, so `10.5/3.1` is `10.5 eV`; with 161 points the grid is 0.13125 eV
  apart.
- **Output.** The columns of `generate.spectral1A` and `generate.spectral1B`
  are the distance along the path in `1/Angstrom`, the energy in units of
  `g0`, and the intensity of sublattice `A` and `B`. The files run over the
  path outside and over the energy grid inside. The same files are written
  for the other sublattices and layers and hold only zeros here; `run.sh`
  removes them.

The plot shows the two sublattices summed and the logarithm of the
intensity, so the weak intensity in the gap between the `pi` and `sigma`
bands is visible.

## See also

- `../constant_energy_map/`, the same system drawn as a constant-energy map
  `I(kx,ky)` over the whole first Brillouin zone.
