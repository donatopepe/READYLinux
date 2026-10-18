SUMMARY = "READY Linux primary console systemd service"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = "file://readylinux-console.service"
FILESEXTRAPATHS:prepend := "${THISDIR}:"
S = "${WORKDIR}"

inherit systemd allarch

SYSTEMD_SERVICE:${PN} = "readylinux-console.service"
SYSTEMD_AUTO_ENABLE:${PN} = "enable"
RDEPENDS:${PN} += "readylinux systemd"

do_install() {
    install -d ${D}${systemd_system_unitdir}
    install -m 0644 ${WORKDIR}/readylinux-console.service ${D}${systemd_system_unitdir}/readylinux-console.service
}

FILES:${PN} += "${systemd_system_unitdir}/readylinux-console.service"
