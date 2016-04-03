from collections import OrderedDict
from .utils import want_unicode, generate_header


class UnicodeDict(OrderedDict):
    def __setitem__(self, key, value):
        OrderedDict.__setitem__(self,
                                want_unicode(key),
                                want_unicode(value))


class Headers(UnicodeDict):
    def add(self, key, value, **params):
        self[key] = generate_header(want_unicode(value),
                                    UnicodeDict(params))
