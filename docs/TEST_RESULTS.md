# Risultati test

## 2026-10-18 — Template evidenze build Yocto

- Template IT/EN `docs/YOCTO_BUILD_EVIDENCE_TEMPLATE*.md` registrano provenienza OE/layer, distro/MACHINE, BitBake, checksum config/immagine, log parse/build, boot QEMU e smoke checks.
- `python -m unittest discover -s tests -v` — PASS, 55 test.
- Compileall, `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh`, `git diff --check` — PASS.
- Nessun build/boot eseguito: BitBake e QEMU assenti.
