# meta-readylinux

Minimal Yocto layer scaffold for READY Linux. This layer is not yet a complete image and does not pin a Yocto release or fetch sources. `LAYERSERIES_COMPAT_readylinux` currently lists candidate series scarthgap, styhead, walnascar, and wrynose; compatibility with these series has not yet been verified by a release-pinned `bitbake -p`.

## Current contents

- `conf/layer.conf`: layer metadata.
- `conf/distro/readylinux.conf`: initial distro policy, inheriting Poky defaults.
- `recipes-core/images/readylinux-image.bb`: minimal image recipe based on `core-image-minimal` with Python 3 and the READY runtime package group.
- `recipes-ready/readylinux/readylinux_0.3.bb`: installs the existing Python application, BASIC runtime, and AI client as a package. The recipe resolves `file://` sources from the repository root through `FILESEXTRAPATHS`; it does not include llama.cpp binaries or model weights.
- `recipes-core/readylinux/`: systemd service starts READY on `/dev/tty1` as a dedicated unprivileged `ready` account, with a persistent writable state directory and systemd filesystem/kernel hardening (`NoNewPrivileges`, private tmp, protected home/system/clock/kernel settings, restricted SUID/SGID and capabilities). The service and getty mask are owned by package `readylinux-console`, which the image recipe installs. The package masks `getty@tty1.service`; this image reserves tty1 for READY, so it does not provide a normal login prompt there.

## Verification and acceptance (Linux build host required)

Run the read-only Debian host probe before using a configured OE tree; it reports missing command prerequisites but installs nothing and does not fetch sources:

```sh
bash scripts/check-yocto-host.sh
```

Use a checked-out, release-pinned Poky/OE-Core tree and add its layer paths plus this repository to `bblayers.conf`. Do not mix release series. The layer intentionally does not clone repositories or download source. `bitbake -p` validates metadata without building the image. A full image build requires the normal Yocto/OE source downloads unless already cached; run it only when explicitly provisioning a build host.

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
# After build, verify downloaded/copied artifact integrity before boot:
bash scripts/verify-image-artifact.sh /path/to/image.wic <sha256-from-trusted-build-record>
# Boot only with matching kernel + target-specific kernel cmdline; no net/host sharing:
READY_QEMU_KERNEL=/path/to/Image READY_QEMU_APPEND='console=ttyS0 root=/dev/vda' \\
  bash scripts/boot-image-qemu.sh /path/to/image.wic <sha256-from-trusted-build-record> pc
```

Run local systemd unit-file syntax validation on a Linux host (does not verify image integration or runtime behavior):

```sh
bash scripts/validate-systemd-unit.sh
```

Acceptance evidence required before calling this layer reproducible:

1. Record exact Poky/OE-Core commit, layer revisions, distro, `MACHINE`, host OS, and BitBake version.
2. Run `bash scripts/validate-yocto-env.sh`; retain successful `bitbake -p` log.
3. Build `readylinux-image` with documented download/cache state; record artifact checksums.
4. Boot image in QEMU for the selected machine; verify READY owns tty1, non-root UID, persisted `/var/lib/readylinux`, and no competing getty.
5. Compute artifact digest with `sha256sum <image>`; retain build/console logs and image in controlled storage, and record paths/checksum in `docs/build-evidence/<run-id>.md`. Never commit image binaries, credentials, or secret-bearing configs.
6. Keep test results and deviations in `docs/TEST_RESULTS.md` (and EN counterpart).

The recipe uses `file://` sources and the Python standard library only. No model weights, AI runtime binaries, or network fetches are part of the image recipe; model/runtime provisioning remains a separate explicit step. The current generic scaffold reserves `/dev/tty1`; a machine-specific serial console is intentionally deferred until an actual BSP/target is selected, because device names and login policy vary. Image build and boot have not been tested in this repository environment (Windows/MSYS; BitBake and QEMU unavailable). Choose and pin one Yocto release and machine before claiming reproducibility.
