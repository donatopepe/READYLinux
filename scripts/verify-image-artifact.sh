#!/usr/bin/env bash
# Check a built image file and expected SHA-256 before a later, explicit QEMU run.
set -euo pipefail

usage() {
    echo "Usage: $0 <image-path> <expected-sha256>" >&2
}

if [[ $# -ne 2 ]]; then
    usage
    exit 2
fi
image_path="$1"
expected_hash="${2,,}"

if [[ ! -f "${image_path}" || ! -s "${image_path}" ]]; then
    echo "ERROR: image must be an existing non-empty regular file: ${image_path}" >&2
    exit 2
fi
if [[ ! "${expected_hash}" =~ ^[0-9a-f]{64}$ ]]; then
    echo "ERROR: expected SHA-256 must be exactly 64 hexadecimal characters." >&2
    exit 2
fi
if ! command -v sha256sum >/dev/null 2>&1; then
    echo "ERROR: sha256sum is unavailable." >&2
    exit 2
fi

actual_hash="$(sha256sum -- "${image_path}" | awk '{print tolower($1)}' | tr -d '\\\\r')"
if [[ "${actual_hash}" != "${expected_hash}" ]]; then
    echo "ERROR: SHA-256 mismatch for ${image_path}" >&2
    echo "Expected: ${expected_hash}" >&2
    echo "Actual:   ${actual_hash}" >&2
    exit 1
fi
printf 'Image verified: %s\nSHA-256: %s\n' "${image_path}" "${actual_hash}"
