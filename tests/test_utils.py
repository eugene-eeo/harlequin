# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import pytest
from cgi import parse_header
from email.utils import unquote
from harlequin.utils import want_unicode, want_bytes, generate_header,\
                            guess, encode_header


def test_want_unicode():
    assert want_unicode('∂') == '∂'
    assert want_unicode('∂'.encode('utf-8')) == '∂'
    assert want_unicode('∂'.encode('punycode'), 'punycode') == '∂'


def test_want_bytes():
    assert want_bytes('∂') == '∂'.encode('utf-8')
    assert want_bytes('∂', 'punycode') == '∂'.encode('punycode')
    assert want_bytes('∂'.encode('punycode')) == '∂'.encode('punycode')


@pytest.mark.parametrize('key', ['key', 'key\'', '"key\\'])
@pytest.mark.parametrize('val', ['val', 'val\'', '"val\\'])
def test_generate_header(key, val):
    header = generate_header(key, {key: val})
    k, params = parse_header(header)
    assert unquote(k), params == (key, {key: val})


def test_encode_header():
    assert encode_header('abc') == 'abc'
    assert encode_header('é')   == '=?utf-8?b?w6k=?='


def test_guess():
    assert guess('f.gif') == ('image/gif', None)
    assert guess('f.txt') == ('text/plain', None)
    assert guess('f', fallback='text/plain') == ('text/plain', None)
