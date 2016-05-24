"""
    harlequin.headers
    ~~~~~~~~~~~~~~~~~

    Implements datastructures for managing headers without
    encoding hassles.

    :copyright: (c) 2016 Eeo Jun
    :license: MIT, see LICENSE for details.
"""

from collections import OrderedDict
from email.utils import getaddresses
from .utils import want_unicode, generate_header, encode_header


class UnicodeDict(OrderedDict):
    """
    A :class:`collections.OrderedDict` subclass that converts
    all keys and values to unicode.
    """
    def __setitem__(self, key, value):
        OrderedDict.__setitem__(self,
                                want_unicode(key),
                                want_unicode(value))


class Headers(UnicodeDict):
    """
    :class:`UnicodeDict` subclass with some header specific
    methods. Internally all headers are converted to unicode.
    """

    def add(self, key, value='', **params):
        """
        Set the value of *key* to *value* and and optionally
        some additional parameters in the form of keyword args:

            >>> h = Headers()
            >>> h.add('X-Key', 'value', param='val')
            >>> h['X-Key']
            'value; param="val"'

        Note that the keys and values of keyword arguments are
        implicitly converted to unicode.
        """
        if not params:
            self[key] = value
            return
        self[key] = generate_header(want_unicode(value),
                                    UnicodeDict(params))

    @property
    def resent(self):
        """
        Returns a boolean depending on whether a ``Resent-Date``
        header is present.
        """
        return 'Resent-Date' in self

    @property
    def sender(self):
        """
        Gets the address of the 'sender'. This is determined
        by looking at the ``Sender`` header and then the
        ``From`` header. Alternatively if a ``Resent-Date``
        header is present, look at ``Resent-Sender`` and
        ``Resent-From``, in that order.
        """
        key, alt = ('Sender', 'From') if not self.resent else \
                   ('Resent-Sender', 'Resent-From')
        value = self.get(key) or self.get(alt)
        _, addr = getaddresses([value])[0]
        return addr

    @property
    def receivers(self):
        """
        Gets a list of addresses to deliver the message to.
        This looks at the ``To``, ``Cc`` and ``Bcc`` headers,
        or their ``Resent-*`` variants if a ``Resent-Date``
        header is present.
        """
        keys = ('To', 'Cc', 'Bcc') if not self.resent else \
               ('Resent-To', 'Resent-Cc', 'Resent-Bcc')
        vals = (v for v in (self.get(key) for key in keys) if v)
        return [addr for _, addr in getaddresses(vals)]


def prepare_mime(mime, headers):
    """
    Inject *headers* into a given *mime* object. A *mime* object
    is any object that is a subclass :class:`email.message.Message`
    or has a similar interface.
    """
    for key in headers:
        if key == 'Bcc' or key == 'Resent-Bcc':
            continue
        del mime[key]
        mime[key] = encode_header(headers[key])
