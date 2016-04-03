import sys


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
