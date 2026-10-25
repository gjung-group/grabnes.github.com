(development)=
# Development guide

The Fortran sources live in the `lanczosKuboCode/Src/` folder of the
[GRABNES code repository](https://github.com/gjung-group/grabnes). This
section collects the development documentation of that repository: the status
of every capability, the validation record, the conventions, and the design
notes behind recent changes.

## Code structure

The main interactions between the modules of the code are illustrated below.

![Main interactions in grabnes code](../assets/images/codeStructure.png)

The program and the modules making up the code are listed in the
{doc}`../reference/index`; the support libraries `math/` and `MIO/` sit
beside them in `lanczosKuboCode/Src/`.

## Testing and reproducibility

```sh
./tests/regression/smoke_test.sh      # build + example 01
./tests/regression/run_examples.sh    # build + examples 01 to 05 + further checks
python3 -m pytest tests/tapw         # TAPW linear-algebra conventions (Python only)
```

The same commands run automatically on GitHub for every push to the
development and main branches (`.github/workflows/regression.yml`).

The scripts build the solver in a temporary directory, never in the source
tree, run the example inputs, and compare the results numerically with the
reference data (bands within 2e-6 eV, DOS within 1e-9 relative). They also
compare the assembled Hamiltonian, entry by entry, with one constructed
independently in Python. Measured results for both compilers are in
{doc}`cluster-build-and-validation`.

## What is supported

| Level | Meaning | Applies to |
| --- | --- | --- |
| Supported | Runs, is documented, and is reproduced by the test suite | The nine examples above (06 to 09 by `run_long_examples.sh`) |
| Independently validated | Additionally checked against an analytic result or a second implementation | Hamiltonian assembly and bands of graphene, hBN monolayer, and twisted bilayers; Kubo DOS of graphene |
| Research / experimental | Present in the source without sufficient validation for general use | Everything else, including transport, TAPW, spin-orbit, Berry curvature, graphene/hBN and multilayer models |

The full classification, capability by capability, is in
{doc}`functionality-status`.

## Known limitations

- One MPI process only; a run with more is refused. Parallelism is by OpenMP,
  with the Intel build.
- The Kubo solver is stochastic: results vary from run to run unless
  `setSeed .true.` and `seedValue` are given.
- The effective moire-potential model of graphene on hBN assembles a hopping
  table that is not exactly Hermitian; the solver reports the size of the
  asymmetry. See the validation document.
- Many input keywords exist only for research workflows and are undocumented.
  The example inputs and READMEs are the reference for the supported ones.

## Finding your way around the source

The quickest way to understand what an input key does is to look it up in
{doc}`../user-guide/input-keys` — its "Read in" column names the source file
and routine — or to grep the sources:

```bash
grep -r "SuperCell ." lanczosKuboCode/Src/
```

## Building for development

Follow the {doc}`../installation` instructions; the build is driven by
`make.sys` (see {doc}`building-documentation` for the documentation build).
The code is parallelized with OpenMP.

## Development documents

```{toctree}
:maxdepth: 2

functionality-status
release-readiness
cluster-build-and-validation
coding-conventions
input-key-renaming-proposal
licensing-audit
citation-checklist
software-paper-outline
pre-announcement-changelog
building-documentation
soc-implementation
hamhopping-restructuring
tapw-chern-optimization
known-issues/berry-curvature
```

| Document | Content |
| --- | --- |
| {doc}`functionality-status` | Every capability classified by the evidence that exists for it |
| {doc}`release-readiness` | Checklist for the first announced release: what is complete, what needs a maintainer decision, what is optional |
| {doc}`cluster-build-and-validation` | Build on Linux, test results for both compilers, defects fixed, independent Hamiltonian validation, parameters, performance |
| {doc}`coding-conventions` | Conventions of the solver sources (modules, routines, the `debug.log` trace, `Section.Name` input keys) and the rules added by the tests |
| {doc}`input-key-renaming-proposal` | Table of the present and former names of the input keys; source of the renaming of October 2026 |
| {doc}`licensing-audit` | The license decision (GPL-3.0-or-later), the notices found, and the open points |
| {doc}`citation-checklist` | What `CITATION.cff` contains and what is deliberately absent |
| {doc}`software-paper-outline` | Outline of a possible software paper |
| {doc}`pre-announcement-changelog` | Chronological log of the consolidation work |
| {doc}`building-documentation` | How to build the Sphinx/Doxygen documentation |
| {doc}`soc-implementation`, {doc}`tapw-chern-optimization`, {doc}`known-issues/berry-curvature` | Notes on research functionality (spin-orbit terms, TAPW, Berry curvature) |
| {doc}`hamhopping-restructuring` | State and plan of the `HamHopping`/`HamOnSite` source restructuring |

Terms used throughout:

- **Implemented**: the code exists.
- **Tested**: it runs and passes defined checks in `tests/regression/`.
- **Independently validated**: results were checked against an analytic
  result or a second implementation.
- **Research / experimental**: present without sufficient validation for
  general use.
