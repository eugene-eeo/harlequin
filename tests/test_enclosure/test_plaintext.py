# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import pytest
from base64 import b64decode
from harlequin.utils import encode_header, want_bytes
from harlequin.enclosure import PlainText, HTML


@pytest.fixture(params=['utf-8', 'punycode'])
def encoding(request):
    return request.param


def test_plaintext_mime_object(encoding):
    content = 'ünicodé'
    p = PlainText(content, encoding=encoding)
    m = p.mime_object()
    assert not m.defects
    assert m.get_content_type() == 'text/plain'
    assert b64decode(want_bytes(m.get_payload())) == \
            content.encode(encoding)


def test_plaintext_mime(encoding):
    content = 'ünicodé'
    headers = [
        ('Sender', 'sender@mail.com'),
        ('X-Key',  'value'),
    ]
    p = PlainText(content, encoding=encoding, headers=headers)
    m = p.mime()
    assert not m.defects
    assert m['X-Key'] == encode_header('value')
    assert m['Sender'] == encode_header('sender@mail.com')


def test_html_type(encoding):
    p = HTML('ünico∂é', encoding=encoding)
    m = p.mime_object()
    assert not m.defects
    assert m.get_content_type() == 'text/html'
