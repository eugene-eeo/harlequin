import sys
import mimetypes
from email.utils import quote
from email.header import Header


if sys.version_info[0] == 3:
    unicode = str
else:
    bytes = str


def want_bytes(s, charset='utf-8'):
    if isinstance(s, bytes):
        return s
    return s.encode(charset)


def want_unicode(s, charset='utf-8'):
    if isinstance(s, unicode):
        return s
    return s.decode(charset)


def generate_header(value, params):
    parts = [quote(value)]
    for key in params:
        parts.append('{k}="{v}"'.format(
            k=key,
            v=quote(params[key]))
            )
    return '; '.join(parts)


def encode_header(string):
    # Don't explicitly specify encoding so that the header
    # class can figure out how to best encode the value.
    # for instance:
    #   >>> Header('one').encode()
    #   'one'
    #   >>> Header('one', charset='utf-8').encode()
    #   '=?utf-8?q?one?='
    return Header(string).encode()


def guess(path, fallback='application/octet-stream'):
    guessed, encoding = mimetypes.guess_type(path, fallback)
    if guessed is None:
        return fallback, encoding
    return guessed, encoding
