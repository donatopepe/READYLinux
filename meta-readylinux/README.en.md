# meta-readylinux

Minimal Yocto layer scaffold for READY Linux. It is not yet a complete image and does not pin a Yocto release or fetch source.

## Contents

- `conf/layer.conf`: layer metadata.
- `conf/distro/readylinux.conf`: initial distro policy inheriting Poky defaults.
- `recipes-core/images/readylinux-image.bb`: minimal image with the READY runtime.
- `recipes-ready/readylinux/readylinux_0.3.bb`: installs the Python console, BASIC runtime, AI client, and vibe workspace code. `FILESEXTRAPATHS` resolves `file://` sources from the repository root; the recipe does not include llama.cpp binaries or model weights.
- `recipes-core/readylinux/`: systemd starts READY on `/dev/tty1` as a dedicated unprivileged `ready` account, with persistent writable state and baseline filesystem hardening. The package masks `getty@tty1.service`; this image reserves tty1 for READY and therefore has no normal login prompt on that terminal.

## Verification and acceptance (Linux build host required)

Use a Linux host with a checked-out, release-pinned Poky/OE-Core tree. Add required OE layers plus `meta-readylinux` in `bblayers.conf`. Do not mix release series. This layer intentionally does not clone repositories or download source. `bitbake -p` validates metadata without building the image. A full image build needs normal Yocto/OE source downloads unless already cached; run only when explicitly provisioning a build host.

```sh
bitbake-layers add-layer /path/to/READYLinux/meta-readylinux
# Run from repository root after sourcing the target's oe-init-build-env:
bash scripts/validate-yocto-env.sh
# Only after metadata parse succeeds, explicitly build the image (may fetch sources):
bitbake readylinux-image
```

No model weights, AI runtime binaries, or network fetches are included by the image recipe; model/runtime provisioning remains a separate explicit step. The generic scaffold reserves `/dev/tty1`; a machine-specific serial console is intentionally deferred until a real BSP/target is selected because device names and login policy vary. Acceptance evidence required before calling this layer reproducible:

1. Record exact Poky/OE-Core commit, layer revisions, distro, `MACHINE`, host OS, and BitBake version.
2. Run `bash scripts/validate-yocto-env.sh`; retain successful `bitbake -p` log.
3. Build `readylinux-image` with documented download/cache state; record artifact checksums.
4. Boot image in QEMU for the selected machine; verify READY owns tty1, non-root UID, persisted `/var/lib/readylinux`, and no competing getty.
5. Store results and deviations in `docs/TEST_RESULTS.en.md` and Italian counterpart.

Build and boot are **not verified here**: current Windows/MSYS environment has no BitBake or QEMU. Pin one Yocto release and target machine before claiming reproducibility. The recipe only uses local `file://` sources; model weights are excluded.
