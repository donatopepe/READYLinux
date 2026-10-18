# READY Linux Yocto Build Evidence Template (EN)

This is the English companion to `YOCTO_BUILD_EVIDENCE_TEMPLATE.md`; use one copy per run at `docs/build-evidence/<run-id>.md`. Machine-readable format is `YOCTO_BUILD_EVIDENCE.schema.json`; an example not-run record is `YOCTO_BUILD_EVIDENCE.example.json`. Do not mark fields verified without retained command output or artifacts.

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
- `conf/local.conf` checksum (redact secrets; never attach credentials):
- `conf/bblayers.conf` checksum:
- `bash scripts/validate-yocto-env.sh` exit code and retained log:
- Confirm parser succeeded; identify retained log:

## Image build

- Command:
- Network/source-cache condition (sources cached or fetched):
- Exit code and retained build log:
- Image artifact path, format, size:
- SHA-256:

## Boot and smoke checks

- QEMU version and exact command / machine arguments:
- Boot result and retained serial/console log:
- READY appears on selected console:
- `id` confirms unprivileged service user:
- `/var/lib/readylinux` writable by READY user and persists after reboot:
- `getty@tty1` mask and no competing login prompt:
- BASIC smoke result:
- Network-disabled/offline smoke result:
- Regressions, deviations, follow-up:

## Verdict

- [ ] Build reproducible from recorded sources/configuration.
- [ ] Image boot verified for this specific machine only.
- [ ] Not verified / blocked (explain):
