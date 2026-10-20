#!/usr/bin/env bash
# Explicit QEMU boot for a verified x86_64 READY image artifact.
# Networking stays disabled unless loopback-only SSH forwarding is explicitly requested.
set -euo pipefail

usage() {
    echo "Usage: $0 <image-path> <expected-sha256> <machine>" >&2
    echo "Example: $0 image.wic <64-hex-sha256> pc" >&2
    echo "Optional SSH test forward: set READY_QEMU_SSH_PORT to a host TCP port; it binds only to 127.0.0.1." >&2
}

if [[ $# -ne 3 ]]; then
    usage
    exit 2
fi
image_path="$1"
expected_hash="${2,,}"
machine="$3"

case "${machine}" in
    pc|q35|microvm) ;;
    *) echo "ERROR: unsupported machine preset '${machine}' (allowed: pc, q35, microvm)." >&2; exit 2 ;;
esac
qemu_bin="${READY_QEMU_BIN:-qemu-system-x86_64}"
qemu_img_bin="${READY_QEMU_IMG:-qemu-img}"
if [[ -z "${READY_QEMU_KERNEL:-}" || ! -f "${READY_QEMU_KERNEL}" ]]; then
    echo "ERROR: set READY_QEMU_KERNEL to the kernel matching this image; no kernel was supplied." >&2
    exit 2
fi
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
    exit 1
fi

if ! command -v "${qemu_bin}" >/dev/null 2>&1 || ! command -v "${qemu_img_bin}" >/dev/null 2>&1; then
    echo "ERROR: qemu-system-x86_64 and qemu-img are required." >&2
    exit 2
fi
if [[ -z "${READY_QEMU_APPEND:-}" ]]; then
    echo "ERROR: set READY_QEMU_APPEND to the kernel cmdline for the selected image/machine." >&2
    exit 2
fi
ssh_forward=()
if [[ -n "${READY_QEMU_SSH_PORT:-}" ]]; then
    if [[ ! "${READY_QEMU_SSH_PORT}" =~ ^[0-9]{1,5}$ ]] || (( READY_QEMU_SSH_PORT < 1 || READY_QEMU_SSH_PORT > 65535 )); then
        echo "ERROR: READY_QEMU_SSH_PORT must be a TCP port from 1 to 65535." >&2
        exit 2
    fi
    ssh_forward=( -nic "user,model=virtio-net-pci,hostfwd=tcp:127.0.0.1:${READY_QEMU_SSH_PORT}-:22" )
else
    ssh_forward=( -nic none )
fi
printf 'Verified image SHA-256: %s\n' "${actual_hash}"
tmp_dir="$(mktemp -d)"
trap 'rm -rf "${tmp_dir}"' EXIT INT TERM
"${qemu_img_bin}" create -q -f qcow2 -F raw -b "${image_path}" "${tmp_dir}/overlay.qcow2"
if [[ -n "${READY_QEMU_SSH_PORT:-}" ]]; then
    echo "Starting QEMU with SSH forwarded only on 127.0.0.1:${READY_QEMU_SSH_PORT} (guest port 22). Disposable COW overlay; no host sharing or monitor."
else
    echo "Starting QEMU (${machine}) using a disposable COW overlay, no network, host sharing, or monitor. Press Ctrl-C to stop."
fi
set +e
"${qemu_bin}" \
    -machine "${machine}" \
    -m 2048 \
    -smp 2 \
    -kernel "${READY_QEMU_KERNEL}" \
    -append "${READY_QEMU_APPEND}" \
    -drive "file=${tmp_dir}/overlay.qcow2,format=qcow2,if=virtio" \
    -display none \
    -serial stdio \
    -monitor none \
    "${ssh_forward[@]}" \
    -no-reboot
qemu_status=$?
set -e
rm -rf "${tmp_dir}"
trap - EXIT INT TERM
exit "${qemu_status}"
