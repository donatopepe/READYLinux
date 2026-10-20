# meta-readylinux

Minimal Yocto layer scaffold for READY Linux. It is not yet a complete image and does not pin a Yocto release or fetch source. `LAYERSERIES_COMPAT_readylinux` currently lists candidate series scarthgap, styhead, walnascar, and wrynose; compatibility with these series has not yet been verified by a release-pinned `bitbake -p`.

## Contents

- `conf/layer.conf`: layer metadata.
- `conf/distro/readylinux.conf`: initial distro policy inheriting Poky defaults.
- `recipes-core/images/readylinux-image.bb`: minimal image with the READY runtime. It also appends `IMAGE_FSTYPES:append = " wic"`, so the documented verification and boot steps receive a `.wic` artifact.
- `recipes-ready/readylinux/readylinux-runtime_0.3.bb`: installs the Python console, BASIC runtime, AI client, and vibe workspace code. `FILESEXTRAPATHS` resolves `file://` sources from the repository root; the recipe does not include llama.cpp binaries or model weights.
- `recipes-core/readylinux/`: systemd starts READY on `/dev/tty1` as a dedicated unprivileged `ready` account, with persistent writable state and systemd filesystem/kernel hardening (`NoNewPrivileges`, private tmp, protected home/system/clock/kernel settings, restricted SUID/SGID and capabilities). The service package `readylinux-console` declares `RDEPENDS:${PN} += "readylinux-runtime systemd"` and includes `readylinux-console.service` plus the getty mask in `FILES:${PN}`; the image recipe installs it. It masks `getty@tty1.service`; this image reserves tty1 for READY and therefore has no normal login prompt on that terminal.

## Verification and acceptance (Linux build host required)

Run the read-only Debian host probe before using a configured OE tree; it reports missing command prerequisites, installs nothing, and fetches no sources:

```sh
bash scripts/check-yocto-host.sh
```

Use a Linux host with a checked-out, release-pinned Poky/OE-Core tree. Add required OE layers plus `meta-readylinux` in `bblayers.conf`. Do not mix release series. This layer intentionally does not clone repositories or download source. `bitbake -p` validates metadata without building the image. A full image build needs normal Yocto/OE source downloads unless already cached; run only when explicitly provisioning a build host.

```sh
cd /path/to/poky
source oe-init-build-env /path/to/build
# Select the READY distro and an explicitly chosen BSP in build/conf/local.conf.
# DISTRO = "readylinux"
# MACHINE = "<selected-bsp-machine>"
bitbake-layers add-layer /path/to/READYLinux/meta-readylinux
cd /path/to/READYLinux
bash scripts/validate-yocto-env.sh
# Only after metadata parse succeeds, explicitly build the image (may fetch sources):
bitbake readylinux-image
# After build, verify copied/downloaded artifact integrity before boot:
bash scripts/verify-image-artifact.sh /path/to/image.wic <sha256-from-trusted-build-record>
# Boot only with matching kernel + target-specific kernel cmdline; no networking/host share:
READY_QEMU_KERNEL=/path/to/Image READY_QEMU_APPEND='console=ttyS0 root=/dev/vda' \\
  bash scripts/boot-image-qemu.sh /path/to/image.wic <sha256-from-trusted-build-record> pc
```

No model weights, AI runtime binaries, or network fetches are included by the image recipe; model/runtime provisioning remains a separate explicit step. The generic scaffold reserves `/dev/tty1`; a machine-specific serial console is intentionally deferred until a real BSP/target is selected because device names and login policy vary. Run local systemd unit syntax validation on a Linux host (this does not verify image integration or runtime behavior):

```sh
bash scripts/validate-systemd-unit.sh
```

Acceptance evidence required before calling this layer reproducible:

1. Record exact Poky/OE-Core commit, layer revisions, distro, `MACHINE`, host OS, and BitBake version.
2. Run `bash scripts/validate-yocto-env.sh`; retain successful `bitbake -p` log.
3. Build `readylinux-image` with documented download/cache state; record artifact checksums.
4. Boot image in QEMU for the selected machine; verify READY owns tty1, non-root UID, persisted `/var/lib/readylinux`, and no competing getty.
5. Compute artifact digest with `sha256sum <image>`; retain image and build/console logs in controlled storage, and record locations/checksum in `docs/build-evidence/<run-id>.md`. Never commit image binaries, credentials, or secret-bearing configs.
6. Store results and deviations in `docs/TEST_RESULTS.en.md` and Italian counterpart.

Build and boot are **not verified here**: current Windows/MSYS environment has no BitBake or QEMU. Pin one Yocto release and target machine before claiming reproducibility. The recipe only uses local `file://` sources; model weights are excluded.
