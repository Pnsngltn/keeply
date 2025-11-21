"""Compatibility shim providing get_python_lib used by older packages.

This re-implements a tiny subset of distutils.sysconfig using sysconfig from
the standard library. It returns paths compatible with what distutils used to
provide.

Only implements what is needed by the `cs50` package import (get_python_lib).
"""
import sysconfig
import os

def get_python_lib(plat_specific=False, prefix=None):
    """Return the path to the site-packages directory.

    plat_specific: when True, return platform-specific library (platlib).
    prefix: ignored in this shim.
    """
    key = "platlib" if plat_specific else "purelib"
    path = sysconfig.get_path(key)
    # Fallback: ensure path exists or derive from sys.prefix
    if path and os.path.isdir(path):
        return path
    # Derive a reasonable fallback
    return sysconfig.get_path('purelib')

# Provide a couple of additional helpers some packages may expect
def get_python_inc(plat_specific=False):
    return sysconfig.get_path('include')
