#!/usr/bin/env python3
"""ARPES spectral function I(k,E) of pristine graphene along the K-Gamma-M-K' path.

    python3 plot.py                 figure graphene_arpes.png (from the run, or from reference/spectral_map.dat)
    python3 plot.py --table FILE    only collect the run into one table (what reference/spectral_map.dat holds)

Table: comment lines with the energy unit g0 and the k path, then one row per point of the path and of the
energy grid: distance along the path [1/Angstrom], energy [eV], intensity of sublattice A, intensity of
sublattice B. The two intensities are what GRABNES writes to generate.spectral1A and generate.spectral1B.
"""

import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT = HERE / "Gendata.in"
SUBLATTICE_A = HERE / "generate.spectral1A"
SUBLATTICE_B = HERE / "generate.spectral1B"
REFERENCE = HERE / "reference" / "spectral_map.dat"
OUTPUT = HERE / "reference" / "graphene_arpes.png"

GREEK = {"gamma": r"$\Gamma$"}


def number(text):
    """One number of an input line, which GRABNES also accepts as a fraction such as 2/3."""
    value = float(text.split("/")[0] or 1.0)
    for divisor in text.split("/")[1:]:
        value /= float(divisor)
    return value


def path_from_input():
    """[(distance along the path, label)] of the Spectral.Path block of Gendata.in.

    GRABNES measures the distance along the path in the reciprocal cell of the reference lattice,
    which for one graphene sheet is the cell of the calculation itself.
    """
    text = INPUT.read_text()
    lattice = re.search(r"^Structure\.LatticeParameter\s+(\S+)", text, re.MULTILINE)
    a = float(lattice.group(1)) if lattice else 2.46
    block = re.search(r"^&begin Spectral\.Path.*?\n(.*?)&end Spectral\.Path", text, re.MULTILINE | re.DOTALL)
    if not block:
        raise SystemExit(f"{INPUT.name}: no Spectral.Path block")
    marks, walked, previous = [], 0.0, None
    for line in block.group(1).splitlines():
        value, _, comment = line.partition("#")
        fractions = value.split()
        if not fractions:
            continue
        f1 = number(fractions[0])
        f2 = number(fractions[1]) if len(fractions) > 1 else 0.0
        point = (f1 * 2 * math.pi / a, (2 * f2 - f1) * 2 * math.pi / (a * math.sqrt(3.0)))
        if previous is not None:
            walked += math.dist(point, previous)
        previous = point
        name = comment.strip()
        marks.append((walked, GREEK.get(name.lower(), name)))
    return marks


def hopping_from_input():
    """The energy unit g0 of the calculation [eV], from TB.Hopping of Gendata.in."""
    match = re.search(r"^TB\.Hopping\s+(\S+)", INPUT.read_text(), re.MULTILINE)
    if not match:
        raise SystemExit(f"{INPUT.name}: no TB.Hopping line: cannot convert the energy axis to eV")
    return float(match.group(1))


def collect():
    """(distances, energies, intensity of A, intensity of B) of a finished run, or None."""
    if not (SUBLATTICE_A.exists() and SUBLATTICE_B.exists()):
        return None
    columns = []
    for path in (SUBLATTICE_A, SUBLATTICE_B):
        rows = [line.split() for line in path.read_text().splitlines() if line.strip()]
        columns.append([[float(value) for value in row] for row in rows])
    g0 = hopping_from_input()
    run = columns[0]
    return ([row[0] for row in run], [row[1] * g0 for row in run],
            [row[2] for row in run], [row[2] for row in columns[1]])
def write_table(path, marks, distances, energies, intensity_a, intensity_b):
    with open(path, "w") as handle:
        handle.write(f"# g0 {hopping_from_input():.6f}\n")
        handle.write("# marks " + ", ".join(f"{distance:.6f} {label}" for distance, label in marks) + "\n")
        handle.write("# columns: path distance [1/A]   E [eV]   I of sublattice A   I of sublattice B\n")
        for distance, energy, first, second in zip(distances, energies, intensity_a, intensity_b):
            handle.write(f"{distance:.6f} {energy:.6f} {first:.6e} {second:.6e}\n")


def read_table(path):
    """(marks, distances, energies, intensity of A, intensity of B) of a table of reference data."""
    marks, rows = [], []
    for line in path.read_text().splitlines():
        if line.startswith("# marks"):
            for item in line.partition("marks")[2].split(","):
                fields = item.split()
                marks.append((float(fields[0]), GREEK.get(fields[1].lower(), fields[1])))
        elif line.strip() and not line.startswith("#"):
            rows.append([float(value) for value in line.split()])
    return marks, [row[0] for row in rows], [row[1] for row in rows], [row[2] for row in rows], [row[3] for row in rows]


def main():
    data = collect()
    if len(sys.argv) > 2 and sys.argv[1] == "--table":
        if data is None:
            raise SystemExit("no finished run in this directory: run ./run.sh first")
        write_table(sys.argv[2], path_from_input(), *data)
        print(f"Wrote {sys.argv[2]}")
        return
    if data is None:
        marks, distances, energies, intensity_a, intensity_b = read_table(REFERENCE)
        source = str(REFERENCE)
    else:
        distances, energies, intensity_a, intensity_b = data
        marks = path_from_input()
        source = "this run"

    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise SystemExit("plot.py requires matplotlib. Install it with: python3 -m pip install matplotlib") from exc

    # The spectral files run over the k path outside and over the energy grid inside, so one k point
    # has a row every <steps> rows and the distance column repeats.
    path = [distances[0]] + [value for previous, value in zip(distances, distances[1:]) if value != previous]
    steps = len(energies) // len(path)
    energies = energies[:steps]
    by_k = []
    for start in range(0, len(intensity_a), steps):
        by_k.append([first + second for first, second in
                     zip(intensity_a[start:start + steps], intensity_b[start:start + steps])])
    brightest = max(max(row) for row in by_k)
    floor = 1e-3 * brightest
    grid = [[math.log10(value + floor) for value in row] for row in zip(*by_k)]

    figure, axis = plt.subplots(figsize=(7.0, 4.4))
    mesh = axis.pcolormesh(path, energies, grid, shading="nearest", cmap="inferno",
                           vmin=math.log10(floor), vmax=math.log10(brightest + floor))
    # The last k point of the run falls one step short of the last vertex of the path.
    for distance, label in marks:
        distance = min(distance, path[-1])
        axis.axvline(distance, color="0.6", linewidth=0.8)
        axis.annotate(label, (distance, 1.0), xycoords=("data", "axes fraction"),
                      ha="center", va="bottom", fontsize=9)
    axis.axhline(0.0, color="0.6", linestyle="--", linewidth=0.8)
    axis.set_xlabel("Distance along the k path (1/Angstrom)")
    axis.set_ylabel("Energy (eV)")
    axis.set_xlim(path[0], min(marks[-1][0], path[-1]))
    axis.set_ylim(energies[0], energies[-1])
    axis.set_title("ARPES spectral function of pristine graphene")
    figure.colorbar(mesh, ax=axis, pad=0.02, label="log intensity (arbitrary units)")
    figure.tight_layout()
    figure.savefig(OUTPUT, dpi=180)
    print(f"Read {source}")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
