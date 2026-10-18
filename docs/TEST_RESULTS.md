# Risultati test

## 2026-10-18 — Hardening unit systemd

- Unit include ProtectClock/KernelLogs/ControlGroups/KernelModules/KernelTunables/Hostname, RestrictSUIDSGID, LockPersonality, RemoveIPC.
- Su copia temporanea WSL systemd 257: `systemd-analyze verify` PASS; `systemd-analyze security --offline` exposure MEDIUM, UMask 0027 lascia file leggibili al gruppo `ready`.
- Suite completa 66 test PASS su Windows/Python 3.11 e WSL/Debian 13/Python 3.13; compileall e shell syntax PASS su entrambi; `git diff --check` PASS.
- BitBake/QEMU non disponibili.
