import pytest
from email.message import Message
from harlequin.enclosure import Enclosure
from harlequin.headers import Headers
from harlequin.utils import encode_header


class CustomEnclosure(Enclosure):
    def mime_object(self):
        return Message()


def test_enclosure_mime_object():
    e = Enclosure()
    with pytest.raises(NotImplementedError):
        e.mime_object()


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
    mime = enclosure.mime()
    assert dict(mime) == {
        'Sender': encode_header('sender@mail.com'),
        'X-Key':  encode_header('value'),
    }