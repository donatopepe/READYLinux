SUMMARY = "Minimal READY Linux image"
LICENSE = "MIT"

require recipes-core/images/core-image-minimal.bb

IMAGE_INSTALL:append = " readylinux-runtime readylinux-console"
