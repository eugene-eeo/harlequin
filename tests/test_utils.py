# -*- coding: UTF-8 -*-
import pytest
from cgi import parse_header
from email.utils import unquote
from harlequin.utils import want_unicode, want_bytes, \
                            generate_header, guess


def test_want_unicode():
    assert want_unicode(u'∂') == u'∂'
    assert want_unicode(u'∂'.encode('utf-8')) == u'∂'
    assert want_unicode(u'∂'.encode('punycode'), 'punycode') == u'∂'


def test_want_bytes():
    assert want_bytes(u'∂') == u'∂'.encode('utf-8')
    assert want_bytes(u'∂', 'punycode') == u'∂'.encode('punycode')
    assert want_bytes(u'∂'.encode('punycode')) == u'∂'.encode('punycode')


@pytest.mark.parametrize('key', ['key', 'key\'', 'key\\'])
@pytest.mark.parametrize('val', ['val', 'val\'', 'val\\'])
def test_generate_header(key, val):
    header = generate_header(key, {key: val})
    k, params = parse_header(header)
    assert unquote(k), params == (key, {key: val})


def test_guess():
    assert guess('f.gif') == ('image/gif', None)
    assert guess('f.txt') == ('text/plain', None)
    assert guess('f', fallback='text/plain') == ('text/plain', None)
