# 10b: Graphene constant-energy ARPES map

The constant-energy photoemission map `I(kx,ky)` of one graphene sheet at
`E = -1.2 eV` over the first Brillouin zone, the ARPES plot of Fig. 8(b) of
Zhu, Shi and MacDonald, arXiv:2006.08908: instead of intensity along a line,
a camera-like picture of all photoelectrons emitted at one energy. The
intensity sits on the warped hexagonal contour `|k - K| = |E|/hbar*v_F`
around all six corners `K+` and `K-` of the zone; along the `Gamma-K`
direction the contour reaches furthest, which is the trigonal warping that
the paper discusses.

## Expected result

![10b: Graphene constant-energy ARPES map](reference/graphene_constant_energy.png)

This is the figure `plot.py` draws from the reference data. After `./run.sh`,
`python3 plot.py` writes `reference/graphene_constant_energy.png` from your
own run; the two figures should look the same.

## How to run

```sh
./run.sh          # or GRABNES_BIN=/path/to/grabnes ./run.sh
python3 plot.py
```

The run takes about one second and writes `generate.spectral1A` and
`generate.spectral1B`: every line holds `kx ky kz E I` for one k point of the
grid, each k point repeated once per energy plane; `plot.py` keeps the plane
at the map energy and adds the two sublattices.

## Method

- **Constant-energy maps.** `Calculate.SpectralEnergyCut .true.` selects
  `DiagSpectralFunctionKGridInequivalentEnergyCut` instead of the k-path
  spectral function of `../spectral_function_path/`. Its k points are a rectangular
  grid, `Diag.KGrid` points per direction, inside a square of half-width
  `Spectral.KGridCut` (in 1/Angstrom) around a center. With
  `Spectral.UseCoordinates .true.` that center is the Cartesian momentum of
  the single point of `Spectral.Path`, here `Gamma`; without it the code
  would use the graphene `K+` valley at `2/3, 1/3` of reciprocal space.
  The map of Fig. 8(b) is centered at `Gamma` and shows the whole zone.
- **Energy planes.** The intensity of one plane sums the states within
  `Spectral.energyGridResolution` (eV) of the plane energy `Spectral.Emin`,
  in units of `g0`. `Kubo.NumberofEnergyPoints 2` is the minimum the code
  accepts; its second plane is a dummy that `plot.py` ignores.
- **Physics.** With nearest-neighbor hopping the Fermi velocity is
  `hbar*v_F = 3*a*g0/2 = 6.58 eV*Angstrom`, so the contour of `E = -1.2 eV`
  lies `0.18 /Angstrom` from each `K`. The warping comes from the trigonal
  term of the linear bands, and the brightness of the contour arcs follows
  from the Wei and Ku matrix element.
- **Other panels of the paper.** For the zoom of Fig. 8(a), the Fermi
  surface at `E = -0.12 eV` near `K+`, set `Spectral.Path` to `1.703 0.0 0.0`
  (`K+` in 1/Angstrom), `Spectral.KGridCut 0.06` and `Spectral.Emin
  0-0.12/3.1`, and keep the same `Diag.KGrid`.

## Files

- `Gendata.in`: the input file.
- `run.sh`: runs GRABNES and removes the sublattice and layer files that a
  single graphene sheet leaves empty.
- `plot.py`: draws `reference/graphene_constant_energy.png` from the run, or from
  `reference/constant_energy_map.dat` when the run is missing;
  `python3 plot.py --all-zones` instead draws the whole square grid, where the
  pattern repeats around every `K + G` (the intensity of the run is periodic
  in the reciprocal lattice, so the blank corners of the default figure are
  a plotting choice, not physics), written to
  `reference/graphene_constant_energy_all_zones.png`;
  `python3 plot.py --table FILE` writes that table from a finished run.
- `reference/`: the table of the map, `E`, `g0` and the lattice constant in
  its header, and the figure drawn from it.

## See also

- `../spectral_function_path/`, the same spectral function along the
  `K-Gamma-M-K'` path.
- `../../2006.08908v3.pdf`, the paper behind this figure.
