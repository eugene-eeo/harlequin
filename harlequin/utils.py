"""
    harlequin.utils
    ~~~~~~~~~~~~~~~

    Heavily tested utility functions for internal use.

    :copyright: (c) 2016 Eeo Jun.
    :license: MIT, see LICENSE for details.
"""

import sys
import mimetypes
from email.utils import quote
from email.header import Header

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


def generate_header(value, params):
    """
    Given *value* and parameters *params* return a string
    suitable for use as a value of a header. Usage
    examples:

        >>> generate_header('value')
        'value'
        >>> generate_header('value', {'param': 'val'})
        'value; param="val"'

    :param value: 'Main' value of the header
    :param params: A dict or mapping of unicode strings.
    """
    parts = [quote(value)]
    for key in params:
        parts.append('%s="%s"' % (key, quote(params[key])))
    return '; '.join(parts)


def encode_header(string):
    """
    Given a unicode *string* encode it for use as a
    value for a header. Internally this delegates
    to :class:`email.header.Header`.
    """
    # Don't explicitly specify encoding so that the header
    # class can figure out how to best encode the value.
    # for instance:
    #   >>> Header('one').encode()
    #   'one'
    #   >>> Header('one', charset='utf-8').encode()
    #   '=?utf-8?q?one?='
    return Header(string).encode()


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
