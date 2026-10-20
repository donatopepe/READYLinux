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

if ! command -v bitbake-layers >/dev/null 2>&1; then
    echo "ERROR: bitbake-layers is not available in PATH; source the target build environment." >&2
    exit 2
fi
layers_report="$(cd "${build_dir}" && bitbake-layers show-layers 2>/dev/null || true)"
if [[ -z "${layers_report}" ]]; then
    echo "ERROR: bitbake-layers show-layers produced no output in ${build_dir}." >&2
    exit 4
fi
layer_line="$(printf '%s\n' "${layers_report}" | grep -F -- "${layer_dir}" | head -n 1 || true)"
if [[ -z "${layer_line}" ]]; then
    echo "ERROR: bitbake-layers does not report ${layer_dir} as a registered layer." >&2
    exit 4
fi
layer_collection="$(printf '%s' "${layer_line}" | awk '{print $1}')"
layer_priority="$(printf '%s' "${layer_line}" | awk '{print $NF}')"
if [[ "${layer_collection}" != "readylinux" ]]; then
    echo "ERROR: layer ${layer_dir} is registered as collection '${layer_collection}', expected 'readylinux'." >&2
    exit 4
fi
if ! [[ "${layer_priority}" =~ ^[0-9]+$ ]]; then
    echo "ERROR: cannot read the registered priority of ${layer_dir} from: ${layer_line}" >&2
    exit 4
fi
printf 'Layer collection: %s (priority %s)\n' "${layer_collection}" "${layer_priority}"

core_line="$(printf '%s\n' "${layers_report}" | awk '$1 == "core" {print; exit}')"
if [[ -z "${core_line}" ]]; then
    echo "ERROR: bitbake-layers does not report a 'core' layer; cannot verify the OE release series." >&2
    exit 4
fi
core_path="$(printf '%s' "${core_line}" | awk '{print $2}')"
core_conf="${core_path}/conf/layer.conf"
if [[ ! -f "${core_conf}" ]]; then
    echo "ERROR: missing ${core_conf}; cannot read LAYERSERIES_COMPAT_core." >&2
    exit 4
fi
core_series_raw="$(grep -E '^[[:space:]]*LAYERSERIES_COMPAT_core[[:space:]]*=' "${core_conf}" | tail -n 1 || true)"
core_series_raw="${core_series_raw#*=}"
core_series_raw="${core_series_raw//\"/}"
layer_series_raw="$(grep -E '^[[:space:]]*LAYERSERIES_COMPAT_readylinux[[:space:]]*=' "${layer_dir}/conf/layer.conf" | tail -n 1 || true)"
layer_series_raw="${layer_series_raw#*=}"
layer_series_raw="${layer_series_raw//\"/}"
matched_series=""
for series in ${core_series_raw}; do
    for supported in ${layer_series_raw}; do
        if [[ "${series}" == "${supported}" ]]; then
            matched_series="${series}"
            break 2
        fi
    done
done
if [[ -z "${matched_series}" ]]; then
    echo "ERROR: OE series (${core_series_raw:-unknown}) is not among LAYERSERIES_COMPAT_readylinux (${layer_series_raw:-none})." >&2
    exit 5
fi
printf 'OE series: %s\n' "${matched_series}"

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

if command -v bitbake-getvar >/dev/null 2>&1; then
    image_fstypes="$(cd "${build_dir}" && bitbake-getvar --recipe readylinux-image --value IMAGE_FSTYPES 2>/dev/null || true)"
    image_fstypes="${image_fstypes//$'\n'/ }"
    case " ${image_fstypes} " in
        *" wic "*)
            printf 'Image fstypes: %s\n' "${image_fstypes}"
            ;;
        *)
            echo "ERROR: IMAGE_FSTYPES for readylinux-image does not include wic (got: ${image_fstypes:-unknown}); verify-image-artifact.sh and boot-image-qemu.sh require a .wic." >&2
            exit 6
            ;;
    esac
else
    echo "NOTE: bitbake-getvar is unavailable; skipped the IMAGE_FSTYPES wic contract check." >&2
fi
