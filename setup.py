# This is mostly taken from future-fstrings.
# Source: https://github.com/asottile-archive/future-fstrings/blob/9b8bea/setup.py
import distutils
import os.path
from textwrap import dedent

from setuptools import setup
from setuptools.command.install import install as _install


cursed_registering_code = dedent(
    """\
    try:
        import cursed_for
        cursed_for.register()
    except ImportError:
        pass
    """
)


class install(_install):
    def initialize_options(self):
        _install.initialize_options(self)
        # Use this prefix to get loaded as early as possible
        name = "aaaaa_" + self.distribution.metadata.name

        contents = "import sys; exec({!r})\n".format(cursed_registering_code)
        self.extra_path = (name, contents)

    def finalize_options(self):
        _install.finalize_options(self)

        install_suffix = os.path.relpath(
            self.install_lib,
            self.install_libbase,
        )
        if install_suffix == ".":
            distutils.log.info("skipping install of .pth during easy-install")
        elif install_suffix == self.extra_path[1]:
            self.install_lib = self.install_libbase
            distutils.log.info(
                "will install .pth to '%s.pth'",
                os.path.join(self.install_lib, self.extra_path[0]),
            )
        else:
            raise AssertionError(
                "unexpected install_suffix",
                self.install_lib,
                self.install_libbase,
                install_suffix,
            )


setup(cmdclass={"install": install})
