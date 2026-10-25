# 11b: hBN constant-energy ARPES map

The constant-energy photoemission map `I(kx,ky)` of one hBN sheet at
`E = -3.5 eV` over the first Brillouin zone. The bands are the `pi` bands of
the honeycomb lattice split by the different on-site energies of the B and N
atoms: a gap of `4.98 eV` with the valence band top at `-2.49 eV` at `K` and
the saddle point at `-3.82 eV` at `M`. At `-3.5 eV`, between the two, the
map shows the six warped hole pockets around the `K` points, each one
stronger on the side facing `M` where the band is flat.

## Expected result

![11b: hBN constant-energy ARPES map](reference/hbn_constant_energy.png)

This is the figure `plot.py` draws from the reference data. After `./run.sh`,
`python3 plot.py` writes `reference/hbn_constant_energy.png` from your own
run; the two figures should look the same.

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

- **hBN as a binary honeycomb.** `Run.TypeOfSystem BoronNitride` cannot be
  used for ARPES yet: its atoms are Species 3 and 4, and the photoemission
  weights of `Spectral.WeiKu` are only implemented for Species 1 and 2, so
  every spectral file holds zeros. This example instead takes
  `Run.TypeOfSystem Graphene` and opens the gap with
  `Potential.AddSublatticeMassterm .true.` and `Potential.SublatticeMassterm
  4.98`, which shifts the two sublattices by `+-2.49 eV`. With
  `TB.Hopping 2.88945`, the BN hopping `-3.11*a + 10.68` at `a = 2.505`, this
  is the BoronNitride Hamiltonian up to a uniform shift of `0.6 eV` (the
  mean of the B and N site energies) and an exchange of the two sublattices;
  the bands and every map are the same, only the energy axis moves.
- **Constant-energy maps.** `Calculate.SpectralEnergyCut .true.` selects the
  same routine as `../../10_graphene_arpes_intensity/constant_energy_map/`:
  a rectangular grid of `Diag.KGrid` points per direction inside a square of
  half-width `Spectral.KGridCut` (1/Angstrom) around the Cartesian momentum
  of the single point of `Spectral.Path`, here `Gamma`, and the intensity of
  the states within `Spectral.energyGridResolution` (eV) of the plane energy
  `Spectral.Emin`. The second of the two planes is a dummy that `plot.py`
  ignores.
- **Physics.** The bands are `E(k) = +-sqrt(m^2 + t^2*|f(k)|^2)` with
  `m = 2.49 eV`. The valence band top at `K` sits exactly at `-m` and lives
  on the lower sublattice, which plays the role of the nitrogen atoms: the
  map is almost entirely `generate.spectral1A`. The trigonal warping of the
  pockets and their bulge towards `M` follow from `|f(k)|`; below the saddle
  point at `-3.82 eV` the six pockets merge into one web.
- **Matrix element.** Wei and Ku wrote the photoemission matrix element for
  graphene; here it treats both sublattices as identical `pz` orbitals, so
  the different cross sections of boron and nitrogen are neglected.

## Files

- `Gendata.in`: the input file.
- `run.sh`: runs GRABNES and removes the sublattice and layer files that a
  single hBN sheet leaves empty.
- `plot.py`: draws `reference/hbn_constant_energy.png` from the run, or from
  `reference/hbn_constant_energy_map.dat` when the run is missing;
  `python3 plot.py --all-zones` instead draws the whole square grid, where the
  pattern repeats around every `K + G` (the intensity of the run is periodic
  in the reciprocal lattice, so the blank corners of the default figure are
  a plotting choice, not physics), written to
  `reference/hbn_constant_energy_all_zones.png`;
  `python3 plot.py --table FILE` writes that table from a finished run.
- `reference/`: the table of the map, `E`, `g0` and the lattice constant in
  its header, and the figure drawn from it.

## See also

- `../../10_graphene_arpes_intensity/constant_energy_map/`, the same map for
  pristine graphene at `E = -1.2 eV`.
