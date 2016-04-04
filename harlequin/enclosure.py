from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from .headers import Headers, prepare_mime


class Enclosure(object):
    def __init__(self, headers=()):
        self.headers = Headers(headers)

    def mime_object(self):
        raise NotImplementedError

    def mime(self):
        mime = self.mime_object()
        encoded = self.headers.encode()
        prepare_mime(mime, encoded)
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
