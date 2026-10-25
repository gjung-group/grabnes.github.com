#!/usr/bin/env python3
"""Constant-energy ARPES map I(kx,ky) of hBN at E = -3.5 eV.

    python3 plot.py                 figure hbn_constant_energy.png (from the run, or from
                                    reference/hbn_constant_energy_map.dat)
    python3 plot.py --all-zones     the same, but over the whole square grid: the pattern of the
                                    first Brillouin zone, repeated around every K + G
    python3 plot.py --table FILE    only collect the run into one table (what the reference file holds)

Table: a header line with the kx grid and a line with the map energy, the energy unit g0 and the
lattice constant, then one line per ky value: ky [1/Angstrom] followed by the intensity of
sublattice A plus sublattice B at every kx.
"""

import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT = HERE / "Gendata.in"
SUBLATTICE_A = HERE / "generate.spectral1A"
SUBLATTICE_B = HERE / "generate.spectral1B"
REFERENCE = HERE / "reference" / "hbn_constant_energy_map.dat"
OUTPUT = HERE / "reference" / "hbn_constant_energy.png"


def value(expression):
    """The value of a number of Gendata.in, which may be a term such as 0-1.2/3.1."""
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


def hexagon(a):
    """The first Brillouin zone of a honeycomb lattice with lattice constant a: its six
    corners, which lie
    at 4*pi/(3a) from Gamma, and the three shortest reciprocal lattice vectors, which bound the
    hexagon through |k.G| <= |G|^2/2."""
    kx, ky = 4.0 * math.pi / (3.0 * a), 2.0 * math.pi / (math.sqrt(3.0) * a)
    corners = [(kx * math.cos(math.radians(60 * i)), kx * math.sin(math.radians(60 * i))) for i in range(6)]
    vectors = [(2.0 * math.pi / a, -2.0 * math.pi / (math.sqrt(3.0) * a)),
               (0.0, 4.0 * math.pi / (math.sqrt(3.0) * a)),
               (2.0 * math.pi / a, 2.0 * math.pi / (math.sqrt(3.0) * a))]
    return corners, vectors


def inside(point, vectors):
    for vector in vectors:
        dot = point[0] * vector[0] + point[1] * vector[1]
        if abs(dot) > 0.5 * (vector[0] ** 2 + vector[1] ** 2) + 1e-12:
            return False
    return True


def collect():
    """(kx list, ky list, intensity matrix) of a finished run, or None."""
    if not (SUBLATTICE_A.exists() and SUBLATTICE_B.exists()):
        return None
    g0, energy, nkx, nky, _ = geometry()
    rows = {}
    for path in (SUBLATTICE_A, SUBLATTICE_B):
        for line in path.read_text().splitlines():
            fields = line.split()
            if len(fields) == 5 and abs(float(fields[3]) * g0 - energy) < 1e-4:
                key = (float(fields[0]), float(fields[1]))
                rows[key] = rows.get(key, 0.0) + float(fields[4])
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

    # Without --all-zones the figure is drawn like the map of the paper: only the first
    # Brillouin zone, the corners of the square grid blanked and the hexagon outlined. The run
    # data is periodic in the reciprocal lattice, so the full grid repeats the pattern around
    # every K + G; --all-zones draws that extended-zone picture.
    allzones = "--all-zones" in sys.argv
    output = OUTPUT.with_name(OUTPUT.stem + "_all_zones.png") if allzones else OUTPUT
    corners, vectors = hexagon(a)
    if allzones:
        grid = intensity
    else:
        grid = [[row[index] if inside((x, y), vectors) else float("nan") for index, x in enumerate(kx)]
                for row, y in zip(intensity, ky)]
    brightest = max(max((v for v in row if v == v), default=0.0) for row in grid)

    figure, axis = plt.subplots()
    mesh = axis.pcolormesh(kx, ky, grid, shading="nearest", cmap="Blues", vmin=0.0, vmax=brightest)
    axis.plot([p[0] for p in corners + corners[:1]], [p[1] for p in corners + corners[:1]],
              color="0.7", linewidth=0.8)
    for label, point in ((r"$K^+$", (4.0 * math.pi / (3.0 * a), 0.0)),
                         (r"$K^-$", (-4.0 * math.pi / (3.0 * a), 0.0)),
                         (r"$\Gamma$", (0.0, 0.0))):
        axis.annotate(label, point, xytext=(4, 4), textcoords="offset points", fontsize=10)
    axis.set_xlabel(r"$k_x$ ($\mathrm{A}^{-1}$)")
    axis.set_ylabel(r"$k_y$ ($\mathrm{A}^{-1}$)")
    axis.set_aspect("equal")
    axis.set_title(f"Constant-energy ARPES map of hBN, E = {energy:.1f} eV"
                   + (" (extended zone)" if allzones else ""))
    figure.colorbar(
        mesh, ax=axis,
        pad=0.02, shrink=0.95,
        label="photoemission intensity (arbitrary units)",
    )
    figure.tight_layout()
    figure.savefig(output, dpi=180)
    print(f"Read {source}")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
