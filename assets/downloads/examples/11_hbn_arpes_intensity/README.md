# 11: hBN ARPES intensity

The photoemission intensity of one hBN sheet. Like example 10, this example
is organized in one folder per picture:

| Folder | Picture | Status |
| --- | --- | --- |
| [`constant_energy_map/`](constant_energy_map/) | Intensity `I(kx,ky)` at `E = -3.5 eV` over the whole first Brillouin zone: the six warped hole pockets around the `K` points of the gapped `pi` bands. | Ready |
| `spectral_function_path/` | Intensity `I(k,E)` along a line of the Brillouin zone. | Work in progress |

Both pictures need the photoemission weights of `Spectral.WeiKu`, which are
implemented for the two sublattices `Species 1` and 2 only. `Run.TypeOfSystem
BoronNitride` labels its atoms `Species 3` and 4, so it yields zero intensity
everywhere; `constant_energy_map/` therefore models hBN as a honeycomb of two
sublattices split by `Potential.SublatticeMassterm`, which is the same
Hamiltonian. The spectral function along a path could use the same model,
but has not been written up yet.

## How to run

```sh
cd constant_energy_map
./run.sh                        # or GRABNES_BIN=/path/to/grabnes ./run.sh
python3 plot.py                 # figure in reference/
```

Without a finished run, `plot.py` draws the figure from the reference data in
`reference/`.
