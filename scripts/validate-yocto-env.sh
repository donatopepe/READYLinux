#!/usr/bin/env bash
# Validate an already initialized Yocto environment without fetching/building.
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"
layer_dir="$(cd "${repo_root}/meta-readylinux" && pwd -P)"
build_dir="$(cd "${BUILDDIR:-/}" 2>/dev/null && pwd -P || true)"

if [[ -z "${BUILDDIR:-}" || ! -d "${BUILDDIR}" || -z "${build_dir}" ]]; then
    echo "ERROR: source the target build environment first (BUILDDIR unset or missing)." >&2
    exit 2
fi
if ! command -v bitbake >/dev/null 2>&1; then
    echo "ERROR: bitbake is not available in PATH; source the target build environment." >&2
    exit 2
fi
if [[ ! -f "${build_dir}/conf/bblayers.conf" ]]; then
    echo "ERROR: missing ${build_dir}/conf/bblayers.conf" >&2
    exit 2
fi
if [[ ! -f "${build_dir}/conf/local.conf" ]]; then
    echo "ERROR: missing ${build_dir}/conf/local.conf" >&2
    exit 2
fi
if ! grep -Fq "${layer_dir}" "${build_dir}/conf/bblayers.conf"; then
    echo "ERROR: add ${layer_dir} to bblayers.conf first." >&2
    exit 2
fi

printf 'Build directory: %s\nLayer: %s\n' "${build_dir}" "${layer_dir}"
echo "Running metadata parse only in build directory (no fetch/image build): bitbake -p"
(
    cd "${build_dir}"
    bitbake -p
)
