# Test Results

## 2026-10-18 — systemd unit hardening

- Unit adds ProtectClock/KernelLogs/ControlGroups/KernelModules/KernelTunables/Hostname, RestrictSUIDSGID, LockPersonality, RemoveIPC.
- On WSL systemd 257 temporary copy: `systemd-analyze verify` PASS; `systemd-analyze security --offline` exposure MEDIUM, residual UMask 0027 (group-readable files).
- Full suite 66 tests PASS on Windows/Python 3.11 and WSL/Debian 13/Python 3.13; compileall and shell syntax pass on both; `git diff --check` PASS.
- BitBake/QEMU unavailable.
