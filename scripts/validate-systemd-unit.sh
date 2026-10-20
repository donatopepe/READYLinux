#!/usr/bin/env bash
# Validate the READY systemd unit syntax on Linux without installing it.
set -euo pipefail

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
