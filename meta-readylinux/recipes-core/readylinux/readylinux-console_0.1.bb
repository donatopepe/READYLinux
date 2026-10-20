SUMMARY = "READY Linux primary console systemd service"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = "file://readylinux-console.service"
FILESEXTRAPATHS:prepend := "${THISDIR}:"
S = "${WORKDIR}"

inherit systemd useradd allarch

SYSTEMD_SERVICE:${PN} = "readylinux-console.service"
SYSTEMD_AUTO_ENABLE:${PN} = "enable"
USERADD_PACKAGES = "${PN}"
GROUPADD_PARAM:${PN} = "--system ready"
USERADD_PARAM:${PN} = "--system --gid ready --home-dir /var/lib/readylinux --no-create-home --shell /sbin/nologin ready"
RDEPENDS:${PN} += "readylinux-runtime systemd"

do_install() {
    install -d ${D}${systemd_system_unitdir}
    install -m 0644 ${WORKDIR}/readylinux-console.service ${D}${systemd_system_unitdir}/readylinux-console.service
    install -d ${D}${sysconfdir}/systemd/system
    ln -s /dev/null ${D}${sysconfdir}/systemd/system/getty@tty1.service
}

FILES:${PN} += "${systemd_system_unitdir}/readylinux-console.service ${sysconfdir}/systemd/system/getty@tty1.service"
