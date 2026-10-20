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

distro_line="$(grep -E '^[[:space:]]*DISTRO[[:space:]]*=' "${build_dir}/conf/local.conf" | tail -n 1 || true)"
if [[ -n "${distro_line}" ]]; then
    distro_value="${distro_line#*=}"
    distro_value="${distro_value//\"/}"
    distro_value="${distro_value//[[:space:]]/}"
    if [[ "${distro_value}" != "readylinux" ]]; then
        echo "ERROR: local.conf selects DISTRO = \"${distro_value}\"; READY requires DISTRO = \"readylinux\"." >&2
        exit 3
    fi
else
    echo "NOTE: conf/local.conf does not set DISTRO; set DISTRO = \"readylinux\" (layer README) before parse." >&2
fi

printf 'Build directory: %s\nLayer: %s\n' "${build_dir}" "${layer_dir}"
echo "Running metadata parse only in build directory (no fetch/image build): bitbake -p"
(
    cd "${build_dir}"
    bitbake -p
)
