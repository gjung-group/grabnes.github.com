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

if [ ! -s generate.spectral1A ]; then
    printf '%s\n' "GRABNES finished without creating a non-empty generate.spectral1A." >&2
    exit 1
fi

# The constant-energy map is also written for the second layer and the other sublattice
# slots, which a single graphene sheet does not have: those files hold only zeros.
rm -f generate.spectral1B generate.spectral2A generate.spectral2B generate.spectral2C
rm -f generate.spectral2D generate.spectral2E generate.spectral2F generate.spectral2G
rm -f generate.spectral2H generate.spectralA

printf '%s\n' "Created $example_dir/generate.spectral1A (the coherent weight sits there in Nishi mode)."
printf '%s\n' "Run 'python3 plot.py' to create reference/graphene_coherent_map.png."
