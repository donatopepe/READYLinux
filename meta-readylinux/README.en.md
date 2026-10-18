# meta-readylinux

Minimal Yocto layer scaffold for READY Linux. It is not yet a complete image and does not pin a Yocto release or fetch source.

## Contents

- `conf/layer.conf`: layer metadata.
- `conf/distro/readylinux.conf`: initial distro policy inheriting Poky defaults.
- `recipes-core/images/readylinux-image.bb`: minimal image with the READY runtime.
- `recipes-ready/readylinux/readylinux_0.3.bb`: installs the Python console, BASIC runtime, AI client, and vibe workspace code.

## Build host integration

Use a Linux host with a checked-out, release-pinned Poky/OE-Core tree. Add required OE layers plus `meta-readylinux` in `bblayers.conf`. Do not mix release series. This layer intentionally does not clone repositories or download source. `bitbake -p` validates metadata without building the image. A full image build needs normal Yocto/OE source downloads unless already cached; run only when explicitly provisioning a build host.

```sh
bitbake-layers add-layer /path/to/READYLinux/meta-readylinux
bitbake -p
bitbake readylinux-image
```

Build and boot are **not verified here**: current Windows/MSYS environment has no BitBake or QEMU. Pin one Yocto release and target machine before claiming reproducibility. The recipe only uses local `file://` sources; model weights are excluded.
