# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.packages.qt_base.package import QtBase, QtPackage

from spack.package import *


class QtWebsocketsPbvr(QtPackage):
    """The Qt WebSockets module provides C++ and QML interfaces for
    WebSocket clients and servers."""

    homepage = "https://github.com/qt/qtwebsockets"
    url = "https://github.com/qt/qtwebsockets/archive/refs/tags/v6.2.4.zip"
    list_url = "https://github.com/qt/qtwebsockets/tags"

    license("LGPL-3.0-only OR GPL-2.0-only")

    version("6.2.4", sha256="c9533942c49b6e0ca3065b0a0325eb9949d61f8bad965f2f55f787198fd8cdad")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("qt-base-pbvr")

    for _v in QtBase.versions:
        v = str(_v)
        depends_on("qt-base-pbvr@" + v, when="@" + v)

    def url_for_version(self, version):
        return f"https://github.com/qt/qtwebsockets/archive/refs/tags/v{version}.zip"

    def cmake_args(self):
        args = super().cmake_args() + []
        return args
