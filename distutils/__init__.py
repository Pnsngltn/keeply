"""Small shim package to provide minimal distutils API used by third-party
packages that import distutils.sysconfig. This is a compatibility shim for
environments where distutils is absent (Python 3.12+).

This file intentionally lives in the project root so it is found before the
stdlib's distutils when running the app from the project directory.
"""

__all__ = ["sysconfig"]
