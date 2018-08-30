# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import pytest
from base64 import b64decode
from harlequin.utils import want_bytes
from harlequin.enclosure import Binary
from harlequin.headers import encode_header, generate_header


@pytest.fixture(scope='module')
def binary():
    return Binary(content=want_bytes('ü'),
                  mimetype='application/octet-stream',
                  encoding='utf-8')


def test_binary_init(binary):
    b = binary
    assert b.content == want_bytes('ü')
    assert b.mimetype == 'application/octet-stream'
    assert b.encoding == 'utf-8'


def test_binary_mime_object(binary):
    b = binary
    m = b.mime_object()
    assert not m.defects
    assert m.get_content_type() == b.mimetype
    assert b64decode(want_bytes(m.get_payload())) == b.content
    assert m['Content-Type'] == generate_header(
        b.mimetype,
        {'charset': b.encoding},
        )


def test_binary_encoder_is_called():
    def traced(m):
        traced.mime = m
        traced.calls += 1

    traced.calls = 0
    b = Binary(want_bytes('ü'), 'application/x-e',
               encoder=traced)
    m = b.mime()
    assert traced.mime is m
    assert traced.calls == 1


def test_headers_priority():
    b = Binary(
        want_bytes('ü'),
        'application/x-encode',
        headers=[
            ('Content-Type', 'application/x-thing'),
        ])
    m = b.mime()
    assert not m.defects
    assert m['Content-Type'] == encode_header('application/x-thing')
    assert m.get_content_type() == 'application/x-thing'
