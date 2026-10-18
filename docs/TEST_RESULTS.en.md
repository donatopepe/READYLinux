# Test Results

## 2026-10-18 — Console service hardening

- Service now uses unprivileged `ready`, `StateDirectory=/var/lib/readylinux`, `NoNewPrivileges`, `PrivateTmp`, `ProtectSystem=strict`, `ProtectHome`, and explicit writable state path.
- useradd recipe creates system group/user.
- `python -m unittest discover -s tests -v` — PASS, 43 tests; `compileall`, `bash -n`, and `git diff --check` — PASS. Static tests verify User, persistent state, and declared hardening.
- BitBake/QEMU unavailable: no metadata parse/build/boot verification.
