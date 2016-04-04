from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from .headers import Headers, prepare_mime


class Enclosure(object):
    def __init__(self, headers=()):
        self.headers = Headers(headers)
        self.content = None

    def mime_object(self):
        raise NotImplementedError

    def mime(self):
        mime = self.mime_object()
        encoded = self.headers.encode()
        prepare_mime(mime, encoded)
        return mime
