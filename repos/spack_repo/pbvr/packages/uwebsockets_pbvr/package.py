from spack.package import *


class UwebsocketsPbvr(Package):
    """uWebSockets: high performance web server / WebSocket library.

    This package installs the uWebSockets headers together with the static
    uSockets library built from the bundled submodule.
    """

    homepage = "https://github.com/uNetworking/uWebSockets"
    git      = "https://github.com/uNetworking/uWebSockets.git"

    license("Apache-2.0")

    version("20.76.0", tag="v20.76.0", submodules=True)

    phases = ["build", "install"]

    depends_on("gmake", type="build")
    depends_on("openssl")
    depends_on("zlib")
    depends_on("c", type="build")
    depends_on("cxx", type="build")

    def build(self, spec, prefix):
        with working_dir("uSockets"):
            make("CC={0}".format(spack_cc), "WITH_LTO=0")

    def install(self, spec, prefix):
        # headers from uWebSockets
        install_tree("src", prefix.include.uWebSockets)

        # headers from bundled uSockets
        install_tree("uSockets/src", prefix.include.uSockets)

        # static library built in uSockets
        mkdirp(prefix.lib)
        install("uSockets/uSockets.a", prefix.lib)

    @property
    def headers(self):
        return find_headers("*", self.prefix.include)

    @property
    def libs(self):
        return find_libraries("uSockets", self.prefix.lib, shared=False)
