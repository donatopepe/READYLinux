#!/usr/bin/env bash
# Read-only preflight for a Debian-based Yocto build host. Installs/downloads nothing.
set -uo pipefail

required_commands=(bash git gcc g++ make python3 chrpath cpio diffstat file gawk ip ping socat texi2any unzip wget xz zstd)
optional_commands=(bitbake bitbake-layers qemu-system-x86_64 sha256sum)
missing=0

if [[ -r /etc/os-release ]]; then
    # shellcheck disable=SC1091
    . /etc/os-release
    printf 'OS: %s (%s)\n' "${PRETTY_NAME:-unknown}" "${ID:-unknown}"
else
    echo 'OS: /etc/os-release unavailable'
fi
printf 'Architecture: %s\n' "$(uname -m 2>/dev/null || echo unknown)"
printf 'CPUs: %s\n' "$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo unknown)"
printf 'BitBake must be supplied by a release-pinned Poky/OE-Core checkout.\n'
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
        missing=1
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

if [[ -n "${BUILDDIR:-}" && -d "${BUILDDIR}" ]]; then
    printf '\nBUILDDIR: %s\n' "${BUILDDIR}"
else
    printf '\nBUILDDIR: unset (source the selected release build environment first)\n'
    missing=1
fi

if [[ "${ID:-}" != debian && "${ID_LIKE:-}" != *debian* ]]; then
    printf '\nNOTE: this probe checks Debian command names; review official Yocto host requirements for this distro.\n'
fi

if (( missing )); then
    echo 'Preflight: INCOMPLETE (read-only; no package changes made).'
    exit 1
fi
echo 'Preflight: required Debian host commands and BUILDDIR found; this does not replace BitBake metadata parse.'
