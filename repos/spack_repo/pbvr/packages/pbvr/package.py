# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform
import re

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from llnl.util.filesystem import install_tree

from spack.package import *
from spack.util.environment import set_env


class Pbvr(MakefilePackage):
    """CS/IS-PBVR is a scientific visualization application designed
    based on Particle-Based Volume Rendering (PBVR). This application
    is capable of multivariate visualization and three-dimensional point cloud visualization
    in addition to standard visualization functions such as volume rendering
    and isosurfaces for 3D volume data obtained from simulations and measuring instruments.
    In addition, the framework for distributed processing of optimized PBVR is characterized
    by the ability to remotely visualize large-scale time-series volume data in remote locations
    at high speed. As a method of remote visualization, you can choose between
    client-server (CS) visualization, which visualizes volume data stored in remote storage,
    and in-situ (IS) visualization, which visualizes simulations simultaneously and
    in the same environment. This application is being developed at the Center
    for Computational Science and e-Systems of the Japan Atomic Energy Agency."""

    phases = ["build", "install"]

    homepage = "https://github.com/CCSEPBVR/CS-IS-PBVR"
    url = "https://github.com/CCSEPBVR/CS-IS-PBVR/archive/refs/tags/v3.5.0.tar.gz"
    git = "https://github.com/CCSEPBVR/CS-IS-PBVR.git"

    maintainers("sakamoto-naohito")

    license("LGPL-3.0-only")

    version(
        "develop",
        branch="feature/WebSocket",
        commit="e7b3cad3985db0efeb9803ca3ad8fe2de7c37cbd",
    )

    variant("client", default=True, description="Build Client Program")
    variant("mpi", default=True, description="Enable MPI Support")
    variant("extended_fileformat", default=True, description="Enable extended fileformat")

    depends_on("gmake", type="build")
    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("mpi", when="+mpi")
    depends_on("qt-base-pbvr@6.2.4+opengl+network~sql", when="+client")
    depends_on("qt-svg-pbvr@6.2.4+widgets", when="+client")
    depends_on("qt-websockets-pbvr@6.2.4", when="+client")
    depends_on("vtk@9.3.1~mpi", when="~mpi")
    depends_on("vtk@9.3.1+mpi", when="+mpi")
    depends_on("uwebsockets-pbvr@20.76.0")

    patch("kvs-conf.patch", when="~client~extended_fileformat")
    patch("kvs-extended-fileformat-conf.patch", when="~client+extended_fileformat")
    patch("kvs-client-conf.patch", when="+client~extended_fileformat")
    patch("kvs-client-extended-fileformat-conf.patch", when="+client+extended_fileformat")
    patch("pbvr-conf.patch", when="~mpi")
    patch("pbvr-conf-mpi.patch", when="+mpi")
    patch("makefile-machime-gcc-omp.patch", when="~mpi")
    patch("makefile-machime-gcc-mpi-omp.patch", when="+mpi")
    patch("uwebsockets.patch")

    def patch(self):
        source_dir = self.stage.source_path
        for root, dirs, files in os.walk(source_dir):
            for fname in files:
                path = os.path.join(root, fname)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                    if "KVS_DIR" in content:
                        filter_file("KVS_DIR", "SPACK_KVS_DIR", path)
                except Exception:
                    pass

    def build(self, spec, prefix):
        with set_env(
            SPACK_KVS_DIR=str(prefix),
            VTK_VERSION="9.3",
            VTK_INCLUDE_PATH=str(spec["vtk"].prefix.include) + "/vtk-9.3",
            VTK_LIB_PATH=str(spec["vtk"].prefix.lib),
            UWEBSOCKETS_INCLUDE=str(spec["uwebsockets-pbvr"].prefix.include),
            UWEBSOCKETS_LIB=str(spec["uwebsockets-pbvr"].prefix.lib),
        ):
            # Build KVS
            build_dir = join_path(self.stage.source_path, "KVS")
            with working_dir(build_dir):
                make()
                make("install")

            # Build Client
            if "+client" in spec:
                qmake = Executable(spec["qt-base-pbvr"].prefix.bin.qmake)
                build_dir = join_path(self.stage.source_path, "Client/build")
                libproxy_plugin_dir=join_path(str(spec["libproxy"].prefix.lib), "libproxy")
                os.makedirs(build_dir)
                with working_dir(build_dir):
                    qmake("../pbvr_client.pro")
                    make()

            # Build Sevrer
            make("-C", "Server/VisModule")
            make("-C", "Server/FunctionParser")
            make("-C", "Server/KVSMLConverter")
            make("-C", "Server/Filter")
            make("-C", "Server")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("Server/pbvr_server", prefix.bin)
        install("Server/Filter/pbvr_filter", prefix.bin)
        install("Server/KVSMLConverter/Example/Release/kvsml-converter", prefix.bin)

        if "+client" in spec:
            install("Client/build/App/pbvr_client", prefix.bin)
            src = self.stage.source_path
            install_tree(os.path.join(src, "Client/build/App/Shader"), os.path.join(prefix.bin, "Shader"))
            install_tree(os.path.join(src, "Client/build/App/Font"), os.path.join(prefix.bin, "Font"))
