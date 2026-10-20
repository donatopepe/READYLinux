SUMMARY = "Minimal READY Linux image"
LICENSE = "MIT"

require recipes-core/images/core-image-minimal.bb

IMAGE_INSTALL:append = " readylinux-runtime readylinux-console"

# The documented verification and boot steps consume a .wic artifact.
IMAGE_FSTYPES:append = " wic"
