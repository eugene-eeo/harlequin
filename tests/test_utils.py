# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import pytest
from cgi import parse_header
from harlequin.utils import want_unicode, want_bytes, guess


def test_want_unicode():
    assert want_unicode('∂') == '∂'
    assert want_unicode('∂'.encode('utf-8')) == '∂'
    assert want_unicode('∂'.encode('punycode'), 'punycode') == '∂'


def test_want_bytes():
    assert want_bytes('∂') == '∂'.encode('utf-8')
    assert want_bytes('∂', 'punycode') == '∂'.encode('punycode')
    assert want_bytes('∂'.encode('punycode')) == '∂'.encode('punycode')


def test_guess():
    assert guess('f.gif') == ('image/gif', None)
    assert guess('f.txt') == ('text/plain', None)
    assert guess('f', fallback='text/plain') == ('text/plain', None)
