#!/usr/bin/env python3
"""Coherent (interlayer-free, two-atom) ARPES map I(kx,ky) of graphene near K+ at E = -0.12 eV.

    python3 plot.py                 figure graphene_coherent_map.png (from the run, or from
                                    reference/coherent_map.dat)
    python3 plot.py --table FILE    only collect the run into one table (what the reference file holds)

Left panel: the map of the Fermi-surface ring around K+, drawn on the azimuthal color wheel so
the intensity modulation along the ring - the interference fringes of Fig. 8(a) of the paper -
is visible as a color rotation. Right panel: the same data as intensity over the azimuthal angle
around K+; every bright pixel falls on the interference curve 1 + cos(arg f(k)) with
f = 1 + exp(i k.a1) + exp(i k.a2), the structure factor of the two-atom lattice.

Table: a header line with the kx grid and a line with the map energy, the energy unit g0 and the
lattice constant, then one line per ky value: ky [1/Angstrom] followed by the coherent intensity
at every kx.
"""

import cmath
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT = HERE / "Gendata.in"
SUBLATTICE_A = HERE / "generate.spectral1A"
REFERENCE = HERE / "reference" / "coherent_map.dat"
OUTPUT = HERE / "reference" / "graphene_coherent_map.png"


def value(expression):
    """The value of a number of Gendata.in, which may be a term such as 0-0.12/3.1."""
    total = 0.0
    for term in re.findall(r"[+-][^+-]+|^[^+-]+", expression):
        quotient = 1.0
        first = True
        for part in term.split("/"):
            if first:
                quotient = float(part)
                first = False
            else:
                quotient /= float(part)
        total += quotient
    return total


def setting(key):
    """The values of the 'Key value ...' line of Gendata.in, as a list of strings. A line that
    starts with '#' is a comment and does not count, so a key may be named in prose."""
    for line in INPUT.read_text().splitlines():
        fields = line.split()
        if fields and fields[0] == key:
            return fields[1:]
    raise SystemExit(f"{INPUT.name}: no {key} line")


def geometry():
    """(g0 in eV, map energy in eV, nkx, nky, lattice constant in A) of Gendata.in."""
    g0 = value(setting("TB.Hopping")[0])
    energy = value(setting("Spectral.Emin")[0]) * g0
    nk = setting("Diag.KGrid")
    return g0, energy, int(nk[0]), int(nk[1]), value(setting("Structure.LatticeParameter")[0])


def collect():
    """(kx list, ky list, intensity matrix) of a finished run, or None. In Nishi mode the
    coherent weight is written entirely to sublattice A, so only that file is read."""
    if not SUBLATTICE_A.exists():
        return None
    g0, energy, nkx, nky, _ = geometry()
    rows = {}
    for line in SUBLATTICE_A.read_text().splitlines():
        fields = line.split()
        if len(fields) == 5 and abs(float(fields[3]) * g0 - energy) < 1e-4:
            rows[(float(fields[0]), float(fields[1]))] = float(fields[4])
    kx = sorted({key[0] for key in rows})
    ky = sorted({key[1] for key in rows})
    if len(kx) != nkx or len(ky) != nky:
        raise SystemExit("the run has a different k grid than Diag.KGrid of Gendata.in")
    return kx, ky, [[rows[(x, y)] for x in kx] for y in ky]


def write_table(path, kx, ky, intensity, energy, g0, a):
    with open(path, "w") as handle:
        handle.write("# kx[1/A] " + " ".join(f"{x:.6f}" for x in kx) + "\n")
        handle.write(f"# E[eV] {energy:.6f} g0[eV] {g0:.6f} a[A] {a:.6f}\n")
        for y, row in zip(ky, intensity):
            handle.write(f"{y:.6f} " + " ".join(f"{number:.4f}" for number in row) + "\n")


def read_table(path):
    """(kx, ky, intensity, energy in eV, g0 in eV, lattice constant in A) of a table of reference data."""
    kx, ky, rows, energy, g0, a = [], [], [], 0.0, 1.0, 2.46
    for line in path.read_text().splitlines():
        if line.startswith("# kx"):
            kx = [float(field) for field in line.split()[2:]]
        elif line.startswith("# E["):
            fields = line.split()
            energy, g0, a = float(fields[2]), float(fields[4]), float(fields[6])
        elif line.strip() and not line.startswith("#"):
            fields = line.split()
            ky.append(float(fields[0]))
            rows.append([float(field) for field in fields[1:]])
    return kx, ky, rows, energy, g0, a


def structure_factor(kx, ky, a):
    """f(k) = 1 + exp(i k.a1) + exp(i k.a2) with a1 = a(1,0) and a2 = a(1/2, sqrt(3)/2)."""
    return 1.0 + cmath.exp(1j * kx * a) + cmath.exp(1j * (kx * a / 2.0 + ky * a * math.sqrt(3.0) / 2.0))


def main():
    data = collect()
    if len(sys.argv) > 2 and sys.argv[1] == "--table":
        if data is None:
            raise SystemExit("no finished run in this directory: run ./run.sh first")
        kx, ky, intensity = data
        g0, energy, _, _, a = geometry()
        write_table(sys.argv[2], kx, ky, intensity, energy, g0, a)
        print(f"Wrote {sys.argv[2]}")
        return
    if data is None:
        kx, ky, intensity, energy, _, a = read_table(REFERENCE)
        source = str(REFERENCE)
    else:
        kx, ky, intensity = data
        _, energy, _, _, a = geometry()
        source = "this run"

    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise SystemExit("plot.py requires matplotlib. Install it with: python3 -m pip install matplotlib") from exc

    kplus = 4.0 * math.pi / (3.0 * a)
    bright = [(x, y, v) for row, y in zip(intensity, ky) for x, v in zip(kx, row) if v > 0.02]

    figure, (mapaxis, ring) = plt.subplots(1, 2, width_ratios=[1.0, 1.15])
    mesh = mapaxis.pcolormesh(kx, ky, intensity, shading="nearest", cmap="hsv", vmin=0.0, vmax=2.0)
    mapaxis.plot(kplus, 0.0, "k+", markersize=9)
    mapaxis.annotate(r"$K^+$", (kplus, 0.0), xytext=(5, 5), textcoords="offset points", fontsize=11)
    mapaxis.set_xlabel(r"$k_x$ ($\mathrm{A}^{-1}$)")
    mapaxis.set_ylabel(r"$k_y$ ($\mathrm{A}^{-1}$)")
    mapaxis.set_aspect("equal")
    mapaxis.set_title(f"Coherent ARPES map near $K^+$, E = {energy:.2f} eV")
    figure.colorbar(mesh, ax=mapaxis, pad=0.02, shrink=0.92, label="intensity (arbitrary units)")

    angles = [math.atan2(y, x - kplus) for x, y, _ in bright]
    values = [v for _, _, v in bright]
    order = sorted(range(len(values)), key=lambda i: angles[i])
    ring.plot([angles[i] for i in order], [values[i] for i in order], ".", color="0.6", markersize=3)
    theory_x = [j / 400.0 * 2.0 * math.pi - math.pi for j in range(401)]
    # the interference curve sampled on a circle of the ring's mean radius: bright pixels
    # sit on 1 + cos(arg f), and arg f depends almost only on the direction from K+
    radii = [math.hypot(x - kplus, y) for x, y, _ in bright]
    mean_r = sum(radii) / len(radii)
    theory_y = [1.0 + math.cos(cmath.phase(structure_factor(kplus + mean_r * math.cos(t),
                                                             mean_r * math.sin(t), a)))
                for t in theory_x]
    ring.plot(theory_x, theory_y, "-", color="crimson", linewidth=1.4,
              label=r"$1+\cos(\arg f(\mathbf{k}))$")
    ring.set_xlabel(r"azimuthal angle around $K^+$ (rad)")
    ring.set_ylabel("intensity")
    ring.set_ylim(-0.05, 2.1)
    ring.legend(loc="upper right")
    ring.set_title("azimuthal interference modulation")
    figure.tight_layout()
    figure.savefig(OUTPUT, dpi=180)
    print(f"Read {source}")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
