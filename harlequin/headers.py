from collections import OrderedDict
from email.utils import getaddresses
from .utils import want_unicode, generate_header, encode_header


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
        key, alt = ('Sender', 'From') if not self.resent else \
                   ('Resent-Sender', 'Resent-From')
        value = self.get(key) or self.get(alt)
        _, addr = getaddresses([value])[0]
        return addr

    @property
    def receivers(self):
        keys = ('To', 'Cc', 'Bcc') if not self.resent else \
               ('Resent-To', 'Resent-Cc', 'Resent-Bcc')
        vals = (v for v in (self.get(key) for key in keys) if v)
        return [addr for _, addr in getaddresses(vals)]


def prepare_mime(mime, headers):
    for key in headers:
        if key == 'Bcc' or key == 'Resent-Bcc':
            continue
        del mime[key]
        mime[key] = encode_header(headers[key])
