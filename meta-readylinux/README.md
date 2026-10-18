# meta-readylinux

Minimal Yocto layer scaffold for READY Linux. This layer is not yet a complete image and does not pin a Yocto release or fetch sources.

## Current contents

- `conf/layer.conf`: layer metadata.
- `conf/distro/readylinux.conf`: initial distro policy, inheriting Poky defaults.
- `recipes-core/images/readylinux-image.bb`: minimal image recipe based on `core-image-minimal` with Python 3 and the READY runtime package group.
- `recipes-ready/readylinux/readylinux_0.3.bb`: installs the existing Python application, BASIC runtime, and AI client as a package. The recipe resolves `file://` sources from the repository root through `FILESEXTRAPATHS`.
- `recipes-core/readylinux/`: systemd service starts READY on `/dev/tty1` as a dedicated unprivileged `ready` account, with a persistent writable state directory and baseline filesystem hardening. The package masks `getty@tty1.service`; this image reserves tty1 for READY, so it does not provide a normal login prompt there.

## Integration (Linux build host required)

Use a checked-out, release-pinned Poky/OE-Core tree and add its layer paths plus this repository to `bblayers.conf`. Do not mix release series. The layer intentionally does not clone repositories or download source. `bitbake -p` validates metadata without building the image. A full image build requires the normal Yocto/OE source downloads unless already cached; run it only when explicitly provisioning a build host.

```sh
bitbake-layers add-layer /path/to/READYLinux/meta-readylinux
bitbake -p
bitbake readylinux-image
```

The recipe uses `file://` sources and the Python standard library only. Image build and boot have not been tested in this repository environment (Windows/MSYS; BitBake and QEMU unavailable). Choose and pin one Yocto release and machine before claiming reproducibility.
