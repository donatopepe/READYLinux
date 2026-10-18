# Test Results

## 2026-10-18 — Yocto build evidence criteria

- IT/EN guides specify evidence for reproducible builds: OE/layer commits, distro/MACHINE, BitBake version, parse/build logs, artifact checksums, QEMU boot and tty/state checks.
- Static bilingual checklist test verifies required items.
- `python -m unittest discover -s tests -v` — PASS, 53 tests.
- compileall, `bash -n`, `git diff --check` — PASS.
- Build/boot not run (BitBake/QEMU unavailable).


## 2026-10-18 — Yocto image/package wiring

- `python -m unittest tests.test_yocto_scaffold -v` — PASS, 6 tests.
- Test checks exact `IMAGE_INSTALL` package set, recipe files exist, and console service `RDEPENDS` include `readylinux systemd`.
- `python -m unittest discover -s tests -v` — PASS, 52 tests; compileall, `bash -n`, `git diff --check` — PASS.
- BitBake unavailable; real metadata package resolution untested.
