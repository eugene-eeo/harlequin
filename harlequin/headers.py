from collections import OrderedDict
from email.utils import getaddresses
from .utils import want_unicode, generate_header


class UnicodeDict(OrderedDict):
    def __setitem__(self, key, value):
        OrderedDict.__setitem__(self,
                                want_unicode(key),
                                want_unicode(value))


class Headers(UnicodeDict):
    def add(self, key, value='', **params):
        if not params:
            self[key] = value
            return
        self[key] = generate_header(want_unicode(value),
                                    UnicodeDict(params))

    @property
    def resent(self):
        return 'Resent-Date' in self

    @property
    def sender(self):
        value = self.get('Sender') or self.get('From')
        _, addr = getaddresses([value])[0]
        return addr
