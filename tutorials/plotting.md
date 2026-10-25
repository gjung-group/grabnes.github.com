# Post-processing and plotting

GRABNES writes plain-text output files that can be read directly with NumPy.
The [`PyToGrabnes.py`](../assets/downloads/PyToGrabnes.py) driver library
provides ready-made helpers (`plotDOS`, `transformBands`,
`plot_electronic_bandstructure`, `plotStructure`, `plotLatticeVectors`,
`plot_onsite_energies`); this page shows what they do under the hood, from
the plotting recipes of the course notebooks.

## Output files

| File | Content |
|---|---|
| `generate.pos` | Atomic positions (and onsite energies for the moiré potential). |
| `generate.bands` / `generate.bands.dat` | Band energies along the requested path. |
| `generate.DOS` | Lanczos recursion DOS (energy in eV; see normalization note below). |
| `generate.diag.DOS` | Diagonalized DOS. |
| `generate.spectral` | Spectral function $A(k,E)$ for band unfolding. |
| `generate.e` | Onsite energies per atom. |

## DOS

```python
import numpy as np
import matplotlib.pyplot as plt

def getDOS(fileName):
    data = np.genfromtxt(fileName)
    return data[:, 0], data[:, 1]

xdata, ydata = getDOS("generate.DOS")
plt.plot(xdata, ydata)
plt.xlabel("E (eV)")
plt.ylabel("DOS (arb. u.)")
```

```{note}
The Lanczos DOS is renormalized by the number of atoms. To compare with the
diagonalization DOS, multiply the Lanczos DOS by twice the number of atoms
and divide by `TB.Hopping`; its energy axis is also in units of `TB.Hopping`.
```

## Band structures

`generate.bands.dat` lists, for each band, the $(k, E)$ points along the
path; band index `nbands/2` is the highest band touching the charge
neutrality region. A minimal reader:

```python
def getBandstructure(dir1, nPlotBands, EShift):
    """Return (kVec, EVec): lists of k and E arrays for the nPlotBands
    bands centered on the middle of the spectrum, shifted by EShift."""
    f = open(dir1 + "/generate.bands.dat")
    i = j = l = 0
    k, E, kVec, EVec = [], [], [], []
    counterPlotBands = 0
    for line in f:
        i += 1
        a = line.split()
        if i == 10:                      # header line with metadata
            nbands = int(a[5])
            nk = int(a[7])
        if i > 16:
            if len(a) == 0:              # blank line separates bands
                j += 0.5
            elif (int(j) == int(nbands/2 - nPlotBands/2 + counterPlotBands)
                  and int(j) < int(nbands/2 + nPlotBands/2)):
                if l < nk:
                    k.append(float(a[0]))
                    E.append(float(a[1]) - EShift)
                    l += 1
                if l == nk:
                    kVec.append(k); EVec.append(E)
                    l = 0; counterPlotBands += 1
                    k, E = [], []
    return kVec, EVec
```

```python
kVec, EVec = getBandstructure(workingDir, nPlotBands=40, EShift=0.302)
for i, (k, E) in enumerate(zip(kVec, EVec)):
    plt.plot(k, E, color="C0", label="GRABNES" if i == 0 else None)
plt.xlabel("k"); plt.ylabel("E (eV)")
```

## Onsite energies (moiré pattern)

For the G/hBN effective model, every second line of `generate.pos` /
`generate.e` holds one sublattice; plotting the onsite energy as color
reveals the moiré pattern:

```python
data = np.genfromtxt("generate.pos")
xdata, ydata = data[:, 0][::2], data[:, 1][::2]
zdata = np.genfromtxt("generate.e")[:, 0][::2]

plt.figure(figsize=(20, 10))
plt.scatter(xdata, ydata, c=zdata, cmap="gist_ncar")
```

## Spectral function cuts (band unfolding)

```python
data = np.genfromtxt("generate.spectral", skip_header=4)
kx, ky, kz = data[:, 0], data[:, 1], data[:, 2]
energy = data[:, 3] * 3.5 - 0.31     # rescale to eV for this parametrization
spectral = data[:, 4]
```

Group the data in blocks of `nEnergy` points per k-point, select the energy
window around the chosen energy, and sum the spectral weight per k-point to
produce constant-energy contours comparable with ARPES.

## Publication-quality styling

The notebooks ship a `latexify()` helper that configures matplotlib for
two-column journal figures (serif fonts, 8 pt, LaTeX rendering, golden-ratio
figure heights); see the
[original notebooks](../assets/downloads/Twistronics2023.ipynb) for the
full snippet.
