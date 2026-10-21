#!/usr/bin/env bash
# Read-only preflight for a Debian-based Yocto build host. Installs/downloads nothing.
# Exit codes: 0 = required commands + BUILDDIR ready, 1 = INCOMPLETE, 2 = not a Linux host.
set -uo pipefail

required_commands=(bash git gcc g++ make python3 chrpath cpio diffstat file gawk ip lz4c patch perl ping socat tar texi2any unzip wget xargs xz zstd)
optional_commands=(bitbake bitbake-layers qemu-system-x86_64 sha256sum)
missing=0
json=0

for argument in "$@"; do
    case "${argument}" in
        --json) json=1 ;;
        *)
            printf 'Usage: %s [--json]\n' "$0" >&2
            exit 64
            ;;
    esac
done

json_escape() {
    local value="$1"
    value="${value//\\/\\\\}"
    value="${value//\"/\\\"}"
    printf '%s' "${value}"
}

json_string_array() {
    local first=1 item
    printf '['
    for item in "$@"; do
        if (( first )); then
            first=0
        else
            printf ', '
        fi
        printf '"%s"' "$(json_escape "${item}")"
    done
    printf ']'
}

json_status_object() {
    local first=1 item boolean
    printf '{'
    for item in "$@"; do
        if (( first )); then
            first=0
        else
            printf ', '
        fi
        if command -v "${item}" >/dev/null 2>&1; then
            boolean=true
        else
            boolean=false
        fi
        printf '"%s": %s' "$(json_escape "${item}")" "${boolean}"
    done
    printf '}'
}

emit_not_a_linux_host() {
    if (( json )); then
        printf '{"schema_version": 1, "os": {"name": "unavailable", "id": "unavailable"}, "arch": "%s", "cpus": %s, "required": {}, "missing_required": [], "optional": {}, "builddir": {"set": false, "path": null}, "verdict": "not-a-linux-host"}\n' \
            "$(json_escape "$(uname -m 2>/dev/null || echo unknown)")" \
            "$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 0)"
        exit 2
    fi
    echo 'OS: /etc/os-release unavailable'
    echo 'WRONG-ENVIRONMENT: this probe only describes a Linux build host; a Windows/shell-interop run is not evidence.'
    echo 'Preflight: NOT-A-LINUX-HOST (read-only; no package changes made).'
    exit 2
}

os_release="${READYLINUX_OS_RELEASE:-/etc/os-release}"
if [[ ! -r "${os_release}" ]]; then
    emit_not_a_linux_host
fi
# shellcheck disable=SC1090
. "${os_release}"

arch="$(uname -m 2>/dev/null || true)"
[[ -n "${arch}" ]] || arch=unknown
cpus="$(getconf _NPROCESSORS_ONLN 2>/dev/null || true)"
[[ "${cpus}" =~ ^[0-9]+$ ]] || cpus=0
missing_required=()
for command in "${required_commands[@]}"; do
    if ! command -v "${command}" >/dev/null 2>&1; then
        missing_required+=("${command}")
        missing=1
    fi
done

if [[ -n "${BUILDDIR:-}" && -d "${BUILDDIR}" ]]; then
    builddir_set=true
else
    builddir_set=false
    missing=1
fi

if (( json )); then
    if (( missing )); then
        verdict='incomplete'
    else
        verdict='ready'
    fi
    if [[ "${builddir_set}" == true ]]; then
        builddir_json="{\"set\": true, \"path\": \"$(json_escape "${BUILDDIR}")\"}"
    else
        builddir_json='{"set": false, "path": null}'
    fi
    printf '{"schema_version": 1, "os": {"name": "%s", "id": "%s"}, "arch": "%s", "cpus": %s, "required": %s, "missing_required": %s, "optional": %s, "builddir": %s, "verdict": "%s"}\n' \
        "$(json_escape "${PRETTY_NAME:-unknown}")" \
        "$(json_escape "${ID:-unknown}")" \
        "$(json_escape "${arch}")" \
        "${cpus}" \
        "$(json_status_object "${required_commands[@]}")" \
        "$(json_string_array "${missing_required[@]}")" \
        "$(json_status_object "${optional_commands[@]}")" \
        "${builddir_json}" \
        "${verdict}"
    (( missing )) && exit 1
    exit 0
fi

printf 'OS: %s (%s)\n' "${PRETTY_NAME:-unknown}" "${ID:-unknown}"
printf 'Architecture: %s\n' "${arch}"
printf 'CPUs: %s\n' "${cpus}"
if command -v bitbake >/dev/null 2>&1 && command -v bitbake-layers >/dev/null 2>&1; then
    printf 'BitBake executables found on PATH.\n'
else
    printf 'BitBake must be supplied by a release-pinned Poky/OE-Core checkout.\n'
fi
if command -v dpkg-query >/dev/null 2>&1; then
    printf 'Installed key package versions:\n'
    for package in gcc python3 git qemu-system-x86 chrpath gawk; do
        version="$(dpkg-query -W -f='${Version}' "${package}" 2>/dev/null || true)"
        if [[ -n "${version}" ]]; then
            printf '  %s %s\n' "${package}" "${version}"
        fi
    done
fi

printf '\nRequired host commands:\n'
for command in "${required_commands[@]}"; do
    if command -v "${command}" >/dev/null 2>&1; then
        printf '  OK      %s\n' "${command}"
    else
        printf '  MISSING %s\n' "${command}"
    fi
done

printf '\nEnvironment tools (not provided by this probe):\n'
for command in "${optional_commands[@]}"; do
    if command -v "${command}" >/dev/null 2>&1; then
        printf '  FOUND   %s\n' "${command}"
    else
        printf '  ABSENT  %s\n' "${command}"
    fi
done

if [[ "${builddir_set}" == true ]]; then
    printf '\nBUILDDIR: %s\n' "${BUILDDIR}"
else
    printf '\nBUILDDIR: unset (source the selected release build environment first)\n'
fi

if [[ "${ID:-}" != debian && "${ID_LIKE:-}" != *debian* ]]; then
    printf '\nNOTE: this probe checks Debian command names; review official Yocto host requirements for this distro.\n'
fi

if (( missing )); then
    echo 'Preflight: INCOMPLETE (read-only; no package changes made).'
    exit 1
fi
echo 'Preflight: required Debian host commands and BUILDDIR found; this does not replace BitBake metadata parse.'
