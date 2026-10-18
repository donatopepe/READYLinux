SUMMARY = "READY Linux immediate programming and local-AI terminal"
DESCRIPTION = "READY console, reduced BASIC runtime, Python workflow and optional local AI client"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = " \
    file://readylinux.py \
    file://basic.py \
    file://ai_local.py \
    file://vibe.py \
"
FILESEXTRAPATHS:prepend := "${THISDIR}/../../../:"
S = "${WORKDIR}"

inherit allarch
RDEPENDS:${PN} += "python3-core python3-difflib python3-crypt python3-json python3-misc python3-netclient python3-shell"

do_install() {
    install -d ${D}${datadir}/readylinux
    install -m 0644 ${WORKDIR}/readylinux.py ${D}${datadir}/readylinux/readylinux.py
    install -m 0644 ${WORKDIR}/basic.py ${D}${datadir}/readylinux/basic.py
    install -m 0644 ${WORKDIR}/ai_local.py ${D}${datadir}/readylinux/ai_local.py
    install -m 0644 ${WORKDIR}/vibe.py ${D}${datadir}/readylinux/vibe.py

    install -d ${D}${bindir}
    cat > ${D}${bindir}/readylinux <<'EOF'
#!/bin/sh
exec python3 /usr/share/readylinux/readylinux.py "$@"
EOF
    chmod 0755 ${D}${bindir}/readylinux
}

FILES:${PN} += "${datadir}/readylinux ${bindir}/readylinux"
