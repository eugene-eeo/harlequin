import sys
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


def encode_header(string, charset='utf-8'):
    return Header(string, charset).encode()
