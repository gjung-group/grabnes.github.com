# 10: Pristine graphene ARPES intensity

The photoemission intensity `I(k,E)` of one graphene sheet, computed with the
spectral function on a k grid instead of the density of states, in the two
pictures an ARPES experiment is read in. Each picture is a separate folder
with its own `Gendata.in`, `run.sh` and `plot.py`:

| Folder | Picture |
| --- | --- |
| [`spectral_function_path/`](spectral_function_path/) | Intensity `I(k,E)` along the `K-Gamma-M-K'` line, as in example 01: Dirac cone at `K`, van Hove singularities at `+-g0`, `sigma` bands near `+-9.3 eV` at `Gamma`. |
| [`constant_energy_map/`](constant_energy_map/) | Intensity `I(kx,ky)` at one energy over the whole first Brillouin zone, Fig. 8(b) of Zhu, Shi and MacDonald, arXiv:2006.08908: the warped hexagonal contour around the six `K` points. |

Both use the same physics: nearest-neighbor graphene with `TB.Hopping 3.1`
and the photoemission matrix element of Wei and Ku,
Phys. Rev. B 95, 085420 (2017). Both runs take about a second.

## How to run

```sh
cd spectral_function_path       # or constant_energy_map
./run.sh                        # or GRABNES_BIN=/path/to/grabnes ./run.sh
python3 plot.py                 # figure in reference/
```

Without a finished run, `plot.py` draws the figure from the reference data in
`reference/`. `examples/make_reference_figures.sh` redraws the figures of all
examples from their reference data alone.
