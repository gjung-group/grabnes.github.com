(reference)=
# API Reference

```{toctree}
:hidden:

units
```

This page is the entry point for the API of the GRABNES Fortran code. The
program is organized as one main program and the modules listed below, in the
`lanczosKuboCode/Src/` folder of the
[code repository](https://github.com/gjung-group/grabnes). The complete
reference — every public procedure with its arguments, generic interfaces,
and public module variables — is generated directly from the sources and
collected on the {doc}`units` page.

For what each module does, see {doc}`../development/index`; for the complete
list of input keys with their types and defaults, see
{doc}`../user-guide/input-keys`.

## Program

| Unit | Source file | Reference |
|---|---|---|
| `grabnes` | `grabnes.f90` | {ref}`api-grabnes` |
| `grabnes_start` | `grabnes_start.F90` | {ref}`api-grabnes_start` |
| `grabnes_end` | `grabnes_end.f90` | {ref}`api-grabnes_end` |

## Modules

| Module | Source file | Reference |
|---|---|---|
| `atoms` | `atoms.F90` | {ref}`api-atoms` |
| `calc` | `calc.F90` | {ref}`api-calc` |
| `cell` | `cell.F90` | {ref}`api-cell` |
| `constants` | `constants.f90` | {ref}`api-constants` |
| `diag` | `diag.F90` | {ref}`api-diag` |
| `gauss` | `gauss.F90` | {ref}`api-gauss` |
| `ham` | `ham.F90` | {ref}`api-ham` |
| `hybrid` | `hybrid.F90` | {ref}`api-hybrid` |
| `interface` | `interface.F90` | {ref}`api-interface` |
| `kubo` | `kubo.F90` | {ref}`api-kubo` |
| `kuboarrays` | `kuboarrays.f90` | {ref}`api-kuboarrays` |
| `kubosubs` | `kubosubs.F90` | {ref}`api-kubosubs` |
| `magf` | `magf.F90` | {ref}`api-magf` |
| `moireBLShift` | `moireBLShift.F90` | {ref}`api-moireblshift` |
| `name` | `name.f90` | {ref}`api-name` |
| `neigh` | `neigh.F90` | {ref}`api-neigh` |
| `parallel` | `parallel.F90` | {ref}`api-parallel` |
| `random` | `random.F90` | {ref}`api-random` |
| `scf` | `scf.F90` | {ref}`api-scf` |
| `tbpar` | `tbpar.f90` | {ref}`api-tbpar` |
| `version` | `version.f90` | {ref}`api-version` |

The folder also holds the `math/` and `MIO/` support libraries — their units
(`math`, `mio`, `mem`, `io`, `file`, `format`, `string`, `parser`, `debug`,
`timer`, `omp`, `mpi`, …) are listed on the {doc}`units` page as well,
together with the template generators `mem_gen`, `type_gen`, and `test_csr`.
The cpp template fragments `MIO/mem_temp.f90` and `MIO/MPI/mpi_type.f90` are
include files with `[_TYPE]` placeholders and cannot be parsed standalone.

```{note}
The reference page is regenerated with
[`tools/gen_api_reference.py`](https://github.com/gjung-group/grabnes.github.com/blob/main/tools/gen_api_reference.py)
(`uv run python tools/gen_api_reference.py`), which parses the sources with
[Ford](https://forddocs.readthedocs.io). The code repository remains the
source of truth — please report any discrepancy so the page can be
regenerated.
```
