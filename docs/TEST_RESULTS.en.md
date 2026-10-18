# Test Results

## 2026-10-18 — systemd hardening policy

- `python -m unittest tests.test_yocto_scaffold -v` — PASS, 6 tests.
- Explicit assertions for non-root User/Group, `NoNewPrivileges`, `ProtectSystem`, `ProtectHome`, `PrivateTmp`, restricted writable state, and absence of elevated capabilities.
- Full suite `python -m unittest discover -s tests -v` — PASS, 52 tests; compileall, `bash -n`, and `git diff --check` — PASS.
- Unit not validated against running systemd or BitBake.
