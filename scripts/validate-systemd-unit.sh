#!/usr/bin/env bash
# Validate the READY systemd unit syntax on Linux without installing it.
set -euo pipefail

security=0
for argument in "$@"; do
    case "${argument}" in
        --security) security=1 ;;
        *)
            printf 'Usage: %s [--security]\n' "$0" >&2
            exit 64
            ;;
    esac
done

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
unit="${repo_root}/meta-readylinux/recipes-core/readylinux/readylinux-console.service"

if ! command -v systemd-analyze >/dev/null 2>&1; then
    echo "ERROR: systemd-analyze is unavailable; install systemd tools on the validation host." >&2
    exit 2
fi
if [[ ! -f "${unit}" ]]; then
    echo "ERROR: missing unit file: ${unit}" >&2
    exit 2
fi

# The target executable is produced by the image recipe. Substitute a harmless
# host executable only in a temporary copy so verify checks unit syntax locally.
tmp_dir="$(mktemp -d)"
trap 'rm -rf "${tmp_dir}"' EXIT
unit_copy="${tmp_dir}/readylinux-console.service"
sed 's#^ExecStart=/usr/bin/readylinux .*#ExecStart=/bin/true#' "${unit}" > "${unit_copy}"
chmod 0644 "${unit_copy}"

echo "Verifying READY systemd unit syntax (host command substituted in temporary copy)."
systemd-analyze verify "${unit_copy}"

if (( security )); then
    max_exposure="${READY_MAX_EXPOSURE:-8.0}"
    report="$(systemd-analyze security --offline=yes "${unit_copy}" 2>&1 || true)"
    exposure="$(printf '%s' "${report}" | awk '/exposure level/ { if (match($0, /[0-9][0-9.]*[.][0-9]/)) print substr($0, RSTART, RLENGTH) }' | tail -n 1)"
    if [[ -z "${exposure}" ]]; then
        echo "ERROR: cannot read the exposure level from: systemd-analyze security --offline=yes" >&2
        exit 2
    fi
    printf 'Exposure level: %s (limit %s)
' "${exposure}" "${max_exposure}"
    if awk -v value="${exposure}" -v limit="${max_exposure}" 'BEGIN { exit !(value > limit) }'; then
        echo "ERROR: exposure ${exposure} exceeds the configured limit ${max_exposure}; tighten the unit before shipping it." >&2
        exit 7
    fi
fi
