#!/usr/bin/env bash
# Validate an already initialized Yocto environment without fetching/building.
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
layer_dir="${repo_root}/meta-readylinux"

if [[ -z "${BUILDDIR:-}" || ! -d "${BUILDDIR}" ]]; then
    echo "ERROR: source the target build environment first (BUILDDIR unset or missing)." >&2
    exit 2
fi
if ! command -v bitbake >/dev/null 2>&1; then
    echo "ERROR: bitbake is not available in PATH; source the target build environment." >&2
    exit 2
fi
if [[ ! -f "${BUILDDIR}/conf/bblayers.conf" ]]; then
    echo "ERROR: missing ${BUILDDIR}/conf/bblayers.conf" >&2
    exit 2
fi
if [[ ! -f "${BUILDDIR}/conf/local.conf" ]]; then
    echo "ERROR: missing ${BUILDDIR}/conf/local.conf" >&2
    exit 2
fi
if ! grep -Fq "${layer_dir}" "${BUILDDIR}/conf/bblayers.conf"; then
    echo "ERROR: add ${layer_dir} to bblayers.conf first." >&2
    exit 2
fi

printf 'Build directory: %s\nLayer: %s\n' "${BUILDDIR}" "${layer_dir}"
echo "Running metadata parse only (no fetch/image build): bitbake -p"
bitbake -p
