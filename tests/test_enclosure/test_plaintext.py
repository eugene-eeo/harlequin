# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import pytest
from base64 import b64decode
from harlequin.utils import encode_header
from harlequin.enclosure import PlainText, HTML


@pytest.fixture(params=['utf-8', 'punycode'])
def encoding(request):
    return request.param


def test_plaintext_mime_object(encoding):
    content = u'ünicodé'
    p = PlainText(content, encoding=encoding)
    m = p.mime_object()
    assert not m.defects
    assert b64decode(m.get_payload()) == content.encode(encoding)
    assert m.get_content_type() == 'text/plain'


def test_plaintext_mime(encoding):
    content = u'ünicodé'
    headers = [
        ('Sender', 'sender@mail.com'),
        ('X-Key',  'value'),
    ]
    p = PlainText(content, encoding=encoding, headers=headers)
    m = p.mime()
    assert not m.defects
    assert m['X-Key'] == encode_header(u'value')
    assert m['Sender'] == encode_header(u'sender@mail.com')


def test_html_type(encoding):
    p = HTML(u'ünico∂é', encoding=encoding)
    m = p.mime_object()
    assert not m.defects
    assert m.get_content_type() == 'text/html'
