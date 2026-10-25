#!/bin/sh
set -eu

example_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
default_bin="$example_dir/../../../lanczosKuboCode/bin/grabnes"
grabnes_bin=${GRABNES_BIN:-$default_bin}

if [ ! -x "$grabnes_bin" ]; then
    printf '%s\n' "GRABNES executable not found or not executable: $grabnes_bin" >&2
    printf '%s\n' "Compile GRABNES first or set GRABNES_BIN=/path/to/grabnes." >&2
    exit 1
fi

cd "$example_dir"
rm -f generate.spectral* job.out
"$grabnes_bin" Gendata.in > job.out

if [ ! -s generate.spectral1A ] || [ ! -s generate.spectral1B ]; then
    printf '%s\n' "GRABNES finished without creating generate.spectral1A and generate.spectral1B." >&2
    exit 1
fi

# The same k path and energy grid is also written for the other sublattices and for layers
# 2 to 4, which a single graphene sheet does not have: those files hold only zeros.
rm -f generate.spectral2A generate.spectral2B generate.spectral2C generate.spectral2D
rm -f generate.spectral2E generate.spectral2F generate.spectral2G generate.spectral2H
rm -f generate.spectral3A generate.spectral3B generate.spectral4A generate.spectral4B
rm -f generate.spectralA

printf '%s\n' "Created $example_dir/generate.spectral1A (sublattice A) and generate.spectral1B (sublattice B)."
printf '%s\n' "Run 'python3 plot.py' to create reference/graphene_arpes.png."
