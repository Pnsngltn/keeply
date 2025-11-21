"""Minimal implementation of distutils.version.StrictVersion

This shim provides enough behavior for packages that import
`distutils.version.StrictVersion` to compare simple dotted version
strings like '1.2.3'. It is not a full replacement for the stdlib
implementation but is sufficient for compatibility.
"""
import re


class StrictVersion:
    """Parse and compare version numbers like '1.2.3'."""

    version_re = re.compile(r"^(\d+)(?:\.(\d+))*([a-zA-Z]\w*)?$")

    def __init__(self, version):
        if isinstance(version, StrictVersion):
            self.version = version.version
            return
        if not isinstance(version, str):
            raise TypeError("version must be a string")
        # Split on dots and convert numeric parts
        parts = version.split('.')
        parsed = []
        for p in parts:
            if p.isdigit():
                parsed.append(int(p))
            else:
                # Keep non-numeric tail as string
                parsed.append(p)
        self.version = tuple(parsed)

    def __repr__(self):
        return f"StrictVersion('{self}')"

    def __str__(self):
        return '.'.join(str(p) for p in self.version)

    # Comparison operators
    def _cmp(self, other):
        if not isinstance(other, StrictVersion):
            other = StrictVersion(str(other))
        # compare tuples elementwise
        a = self.version
        b = other.version
        # extend shorter with zeros for numeric comparison
        maxlen = max(len(a), len(b))
        a_ext = list(a) + [0] * (maxlen - len(a))
        b_ext = list(b) + [0] * (maxlen - len(b))
        return (a_ext > b_ext) - (a_ext < b_ext)

    def __eq__(self, other):
        return self._cmp(other) == 0

    def __ne__(self, other):
        return self._cmp(other) != 0

    def __lt__(self, other):
        return self._cmp(other) < 0

    def __le__(self, other):
        return self._cmp(other) <= 0

    def __gt__(self, other):
        return self._cmp(other) > 0

    def __ge__(self, other):
        return self._cmp(other) >= 0
