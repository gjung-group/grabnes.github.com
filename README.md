# grabnes.github.com

<p align="center">
  <img src="assets/static/logo1.png" alt="GRABNES logo" width="480">
</p>

The reconstructed website (static page) for grabnes.

The website will feature the following:
- Detailed theory of the implemented features for a wide variety of systems.
- Benchmark studies
- Detailed tutorials (Featuring the examples already included under grabnes/examples/*)
- Development guide

## Current state

The site is a Sphinx documentation tree whose **source directory is the
repository root**, built with MyST-Markdown, the Furo theme, and
sphinx-design, and deployed to GitHub Pages by a GitHub Actions workflow.
Content comes from two sources: the old (2022) Sphinx tree that used to live
in `grabnes/` (being retired), and the
[GRABNES code repository](https://github.com/gjung-group/grabnes)
(`docs/` and `examples/`, mirrored October 2026).

Sections:

| Folder | Content |
| --- | --- |
| `index.md`, `installation.md` | landing page, compile & Colab instructions |
| `theory/` | tight-binding models, moiré supercells, observables, TAPW procedure |
| `examples/` | the supported examples of the code repository (01–13) with figures and downloadable inputs |
| `tutorials/` | graphene, bilayer/graphite, twisted bilayer, graphene on hBN, input flags, plotting |
| `user-guide/` | input-file format, the complete input-key reference, TAPW + SOC input |
| `benchmarks/` | benchmark studies (tBG flat bands, graphite, ARPES) + "coming soon" stubs |
| `development/` | code structure, functionality status, validation record, conventions |
| `reference/` | API reference entry page + generated Fortran unit reference |
| `assets/` | all images, downloadable inputs/scripts, and static CSS |

## Building locally

```bash
uv sync                                        # creates .venv from pyproject/uv.lock
uv run sphinx-build -b html . _build           # open _build/index.html
```

The CI build treats warnings as errors; check with
`uv run sphinx-build -b html -W --keep-going . _build` before committing.

## Deployment

The live site is at <https://gjung-group.github.io/grabnes.github.com/>.
`.github/workflows/docs.yml` builds the site to `public/` on every push to
`main` and uploads it to GitHub Pages (Settings → Pages → "GitHub Actions").
