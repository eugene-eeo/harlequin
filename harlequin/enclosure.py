"""
    harlequin.enclosure
    ~~~~~~~~~~~~~~~~~~~

    Implements enclosure objects.

    :copyright: (c) 2016 Eeo Jun.
    :license: MIT, see LICENSE for details.
"""

from os.path import basename
from email.encoders import encode_base64
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from .headers import Headers, prepare_mime
from .utils import guess


class Enclosure(object):
    """
    Base enclosure object. Enclosure objects encapsulate
    content and headers, and initialise the appropriate
    MIME object.

    :param headers: List/mapping of header to values.
        This will override any headers set by the
        `mime_object` method.
    """

    def __init__(self, headers=()):
        self.headers = Headers(headers)

    def mime_object(self):
        """
        Creates the base MIME object. Default headers
        are to be applied to the MIME object here.
        """
        raise NotImplementedError

    @property
    def sender(self):
        """
        Alias for the ``sender`` property of the
        internal headers object.
        """
        return self.headers.sender

    @property
    def receivers(self):
        """
        Alias for the ``receivers`` property of the
        internal headers object.
        """
        return self.headers.receivers

    def mime(self):
        """
        Returns the finalised MIME object with the
        headers specified in ``__init__`` applied.
        """
        mime = self.mime_object()
        prepare_mime(mime, self.headers)
        return mime


class Collection(Enclosure):
    """
    Represents a multipart MIME object. Collection
    objects can be nested inside one another.

    :param enclosures: A container of enclosure
        objects to be attached.
    """

    def __init__(self, enclosures, **kwargs):
        self.subtype = kwargs.pop('subtype', 'mixed')
        self.enclosures = enclosures
        Enclosure.__init__(self, **kwargs)

    def mime_object(self):
        mime = MIMEMultipart(self.subtype)
        for item in self.enclosures:
            mime.attach(item.mime())
        return mime


class PlainText(Enclosure):
    """
    Represents a MIME object of the `text/plain`
    subtype, with *content* and an optional
    *encoding*.

    :param content: A unicode/byte string.
    :param encoding: Name of encoding to be used.
        If a byte string is provided in *content*
        then *content* must be able to be decoded
        by *encoding*. Else the unicode string is
        encoded using *encoding*.
    """

    subtype = 'plain'

    def __init__(self, content, encoding='utf-8', **kwargs):
        Enclosure.__init__(self, **kwargs)
        self.content = content
        self.encoding = encoding

    def mime_object(self):
        return MIMEText(self.content,
                        self.subtype,
                        self.encoding)


class HTML(PlainText):
    """
    :class:`PlainText` subclass with a mimetype of
    ``text/html``.
    """

    subtype = 'html'


class Binary(Enclosure):
    """
    Represents an enclosure object around some binary
    string/content *content*.

    :param content: Byte string containing content.
    :param mimetype: MIME-type of the content.
    :param encoding: Encoding/charset of the content.
    :param encoder: Encoder function, defaults to
        :func:`email.encoders.encode_base64`. It
        will be passed the created MIME object
        for mutation.
    :param headers: Optional headers.
    """

    def __init__(self, content, mimetype, encoding=None,
                 encoder=encode_base64, **kwargs):
        Enclosure.__init__(self, **kwargs)
        self.content = content
        self.mimetype = mimetype
        self.encoding = encoding
        self.encoder = encoder

    def mime_object(self):
        args = {}
        if self.encoding:
            args['charset'] = self.encoding
        mime = MIMEBase(*self.mimetype.split('/'), **args)
        mime.set_payload(self.content)
        self.encoder(mime)
        return mime


class BinaryFile(Binary):
    """
    Represents a :class:`Binary` enclosure with the
    contents read from a given *path*. The main
    advantage of this class is that the content
    is lazily read and the mimetype and encoding
    is automatically guessed.
    """

    def __init__(self, path, headers=()):
        self.path = path
        self.mimetype, self.encoding = guess(path)
        self.encoder = encode_base64
        self.headers = Headers(headers)

    @property
    def content(self):
        with open(self.path, 'rb') as f:
            return f.read()
