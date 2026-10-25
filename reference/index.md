(api-reference)=
# API Reference

This page is the entry point for the API of the GRABNES Fortran code. The
program is organized as one main program and the modules listed below. The
old website documented these units automatically from the sources with
`sphinx-fortran`; that tooling is no longer maintained, so the detailed
per-unit documentation (procedures, arguments, and derived types extracted
from the sources) will be regenerated and is marked *pending* until then.

For what each module does, see {doc}`../development/index`; for the input
flags that drive these routines, see {doc}`../tutorials/input-reference`.

## Program

| Unit | Source file | Documentation |
|---|---|---|
| `grabnes` | `grabnes.f90` | pending |

## Modules

| Module | Source file | Documentation |
|---|---|---|
| `atoms` | `atoms.f90` | pending |
| `calc` | `calc.f90` | pending |
| `cell` | `cell.f90` | pending |
| `constants` | `constants.f90` | pending |
| `diag` | `diag.f90` | pending |
| `gauss` | `gauss.f90` | pending |
| `ham` | `ham.f90` | pending |
| `hybrid` | `hybrid.f90` | pending |
| `interface` | `interface.f90` | pending |
| `kubo` | `kubo.f90` | pending |
| `kuboarrays` | `kuboarrays.f90` | pending |
| `kubosubs` | `kubosubs.f90` | pending |
| `magf` | `magf.f90` | pending |
| `math` | `math.f90` | pending |
| `name` | `name.f90` | pending |
| `neigh` | `neigh.f90` | pending |
| `parallel` | `parallel.f90` | pending |
| `random` | `random.f90` | pending |
| `scf` | `scf.f90` | pending |
| `tbpar` | `tbpar.f90` | pending |
| `version` | `version.f90` | pending |

```{note}
The unit list above is taken from the previous code documentation. If a unit
has been added, renamed, or removed in the code repository, the code
repository is the source of truth — please report the discrepancy so this
page can be updated.
```
