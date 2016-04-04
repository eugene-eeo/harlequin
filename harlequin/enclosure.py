from os.path import basename
from email.encoders import encode_base64
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

from .headers import Headers, prepare_mime
from .utils import guess


class Enclosure(object):
    def __init__(self, headers=()):
        self.headers = Headers(headers)

    def mime_object(self):
        raise NotImplementedError

    @property
    def sender(self):
        return self.headers.sender

    @property
    def receivers(self):
        return self.headers.receivers

    def mime(self):
        mime = self.mime_object()
        prepare_mime(mime, self.headers)
        return mime


class PlainText(Enclosure):
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
    subtype = 'html'


class Binary(Enclosure):
    def __init__(self, content, mimetype, encoding=None,
                 encoder=encode_base64, **kwargs):
        Enclosure.__init__(self, **kwargs)
        self.content = content
        self.mimetype = mimetype
        self.encoding = encoding
        self.encoder = encoder

    def mime_object(self):
        mime = MIMEBase(*self.mimetype.split('/'))
        mime.set_payload(self.content)
        if self.encoding:
            del mime['Content-Type']
            mime.add_header('Content-Type',
                            self.mimetype,
                            charset=self.encoding)
        self.encoder(mime)
        return mime


class Attachment(Binary):
    def __init__(self, path, headers=()):
        self.path = path
        self.mimetype, self.encoding = guess(path)
        self.encoder = encode_base64
        heads = Headers()
        heads.add('Content-Disposition', 'attachment',
                  filename=basename(path))
        heads.update(headers)
        self.headers = heads

    @property
    def content(self):
        with open(self.path, 'rb') as f:
            return f.read()
