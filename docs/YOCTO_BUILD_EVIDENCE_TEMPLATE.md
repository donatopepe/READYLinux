# READY Linux Yocto Build Evidence

Copy this file per build run to `docs/build-evidence/<run-id>.md`. Machine-readable format is `YOCTO_BUILD_EVIDENCE.schema.json`; `YOCTO_BUILD_EVIDENCE.example.json` contains placeholders only. Do not mark a field verified without a retained command result or artifact; redact credentials before storing evidence.

## Identity

- Run ID / UTC date:
- Host OS and architecture:
- Poky/OE-Core repository URL and exact commit:
- Other layer URLs and exact commits:
- READY Linux repository commit:
- BitBake version:
- Distro:
- `MACHINE` / BSP and revision:
- `TCLIBC` / init system:

## Environment and parse

- Build directory:
- `conf/local.conf` checksum (redact secrets; do not attach credentials):
- `conf/bblayers.conf` checksum:
- `bash scripts/validate-yocto-env.sh` exit code and retained log:
- Confirm parser returned success; attach/identify log:

## Image build

- Command:
- Network/source-cache condition (sources already cached or fetched):
- Exit code and retained build log:
- Image artifact path, format, size:
- SHA-256:

## Boot and smoke checks

- QEMU version and exact command / machine arguments:
- Boot exit/status and retained serial/console log:
- READY appears on selected console:
- `id` confirms service runs unprivileged:
- `/var/lib/readylinux` writable by READY user and persistent after reboot:
- `getty@tty1` mask and absence of competing login prompt:
- BASIC smoke result:
- Network-disabled / offline smoke result:
- Regressions, deviations, follow-up:

## Verdict

- [ ] Build reproducible from recorded sources/configuration.
- [ ] Image boot verified for this specific machine only.
- [ ] Not verified / blocked (explain):
