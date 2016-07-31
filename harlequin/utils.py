"""
    harlequin.utils
    ~~~~~~~~~~~~~~~

    Utility functions for internal use.

    :copyright: (c) 2016 Eeo Jun.
    :license: MIT, see LICENSE for details.
"""

from __future__ import unicode_literals

import sys
import mimetypes

PY3 = sys.version_info[0] == 3
unicode = str if PY3 else unicode
bytes   = bytes if PY3 else str


def want_bytes(s, charset='utf-8'):
    """
    Returns *s* if it is a byte string specific to Python
    versions, else encodes it with the given *charset*.
    """
    if isinstance(s, bytes):
        return s
    return s.encode(charset)


def want_unicode(s, charset='utf-8'):
    """
    Given *s*, return it if it is a unicode string
    specific to Python versions, else decode the
    byte string with the given *charset*.
    """
    if isinstance(s, unicode):
        return s
    return s.decode(charset)


def guess(path, fallback='application/octet-stream'):
    """
    Guess the mimetype and encoding for a given *path*,
    returning *fallback* if it cannot be guessed.
    *fallback* defaults to ``application/octet-stream``.
    """
    guessed, encoding = mimetypes.guess_type(path, fallback)
    if guessed is None:
        return fallback, encoding
    return guessed, encoding
