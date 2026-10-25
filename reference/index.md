(api-reference)=
# API Reference

This page is the entry point for the API of the GRABNES Fortran code. The
program is organized as one main program and the modules listed below, in the
`lanczosKuboCode/Src/` folder of the
[code repository](https://github.com/gjung-group/grabnes). In the repository
the per-unit API pages are generated from the sources with Doxygen and
Breathe; the detailed documentation is *pending* here until it is published.

For what each module does, see {doc}`../development/index`; for the complete
list of input keys with their types and defaults, see
{doc}`../user-guide/input-keys`.

## Program

| Unit | Source file | Documentation |
|---|---|---|
| `grabnes` | `grabnes.f90` | pending |
| `grabnes_start` | `grabnes_start.F90` | pending |
| `grabnes_end` | `grabnes_end.f90` | pending |

## Modules

| Module | Source file | Documentation |
|---|---|---|
| `atoms` | `atoms.F90` | pending |
| `calc` | `calc.F90` | pending |
| `cell` | `cell.F90` | pending |
| `constants` | `constants.f90` | pending |
| `diag` | `diag.F90` | pending |
| `gauss` | `gauss.F90` | pending |
| `ham` | `ham.F90` | pending |
| `hybrid` | `hybrid.F90` | pending |
| `interface` | `interface.F90` | pending |
| `kubo` | `kubo.F90` | pending |
| `kuboarrays` | `kuboarrays.f90` | pending |
| `kubosubs` | `kubosubs.F90` | pending |
| `magf` | `magf.F90` | pending |
| `moireBLShift` | `moireBLShift.F90` | pending |
| `name` | `name.f90` | pending |
| `neigh` | `neigh.F90` | pending |
| `parallel` | `parallel.F90` | pending |
| `random` | `random.F90` | pending |
| `scf` | `scf.F90` | pending |
| `tbpar` | `tbpar.f90` | pending |
| `version` | `version.f90` | pending |

The folder also holds the `math/` and `MIO/` support libraries, and
`test_sparse_diag.F90`.

```{note}
The unit list above was taken from the current `lanczosKuboCode/Src/` folder.
The code repository is the source of truth — please report any discrepancy so
this page can be updated.
```
