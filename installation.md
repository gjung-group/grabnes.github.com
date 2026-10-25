# Installation

The code is maintained on GitHub, where you are free to clone or fork the
stable or development versions of the code (see the GitHub documentation on
how to do this).

## Compiling from source

GRABNES is a plain Fortran code with an OMP-parallelized build path. To
install the code:

1. Modify the `make.sys` file to match the compilers available on your
   system. The code has currently been tested with Intel compilers; gfortran
   builds are also possible.
2. Add an empty `.version` file in the same folder as the `make.sys` file.
3. Build:

   ```bash
   make clean
   make
   ```

The resulting `grabnes` executable reads a single input file (`Gendata.in` by
convention) and writes all output files (`generate.*`) in the working
directory.

```{note}
Input-file convention: negative numbers must be written as `0.0-1.0` rather
than `-1.0`, i.e. `0.0-12.0` means $-12.0$. The parser does not require any
specific ordering of the flags.
```

## Running without installing: Google Colab

A stable build of the code is available on Google Colab, where the code can
be driven from a Python Jupyter notebook. This is the fastest way to follow
the tutorials without dealing with compilers:

```{button-link} https://colab.research.google.com/drive/12_ofrjJi4pr6U9j-ER1WocYJkqxEffs-?usp=sharing
:color: primary

Twistronics 2023 workshop notebook (Google Colab)
```

For production work we recommend compiling the code on your own computational
resources to leverage the OMP capabilities of the code.

## Related packages

Several other real-space tight-binding packages exist, each with its own
strengths, so one may be more suitable than another for the calculation of
specific observables. In alphabetical order:

- [Kwant](https://kwant-project.org/)
- [PyBinding](https://docs.pybinding.site/en/stable/)
- [PythTB](http://www.physics.rutgers.edu/pythtb/#)
- [Quantum-Kite](https://quantum-kite.com/)
- [TBPLaS](http://www.tbplas.net/)
- [Twister](https://github.com/qtm-iisc/Twister)

Related code from associated researchers:
[JeilJungGroupCodes](https://github.com/gjung-group/JeilJungGroupCodes.git).
