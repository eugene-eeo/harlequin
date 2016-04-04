import pytest
from email.message import Message
from harlequin.enclosure import Enclosure
from harlequin.headers import Headers


class CustomEnclosure(Enclosure):
    def mime_object(self):
        return Message()


def test_enclosure_headers():
    args = [('X-Key', 'value')]
    enclosure = CustomEnclosure(args)
    assert enclosure.headers == Headers(args)


def test_enclosure_mime():
    headers = [
        ('Sender', 'sender@mail.com'),
        ('X-Key', 'value'),
    ]
    enclosure = CustomEnclosure(headers)
    encoded = enclosure.headers.encode()
    mime = enclosure.mime()
    placed = dict(mime)
    assert placed == encoded
