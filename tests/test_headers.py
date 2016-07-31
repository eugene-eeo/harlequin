# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import pytest
from email.message import Message
from email.header import decode_header
from email.utils import unquote
from cgi import parse_header
from harlequin.utils import want_bytes, want_unicode
from harlequin.headers import (
        UnicodeDict, Headers,
        inject_headers, encode_header,
        generate_header
        )


def test_unicodedict_init():
    u = UnicodeDict([
        (want_bytes('One'), want_bytes('1'))
    ])
    assert u['One'] == '1'


def test_unicodedict_setitem():
    u = UnicodeDict()
    u[want_bytes('One')] = want_bytes('1')
    assert u['One'] == '1'


@pytest.mark.parametrize('value',  ['Value', want_bytes('Value')])
@pytest.mark.parametrize('params', [
    {},
    {'param': 'value'},
    {'param': want_bytes('value')},
])
def test_headers_add(value, params):
    v, p = want_unicode(value), UnicodeDict(params)
    h = Headers()
    h.add('Key', value, **params)
    assert parse_header(h['Key']) == (v, p)


def test_headers_resent():
    h = Headers()
    h.add('Resent-Date')
    assert h.resent


@pytest.fixture(params=[True, False])
def resent(request):
    return request.param


@pytest.fixture
def headers(resent):
    default = [
        ('From',   '{r}from@mail.com'),
        ('Sender', '{r}sender@mail.com'),
        ('To',     '{r}to@mail.com'),
        ('Cc',     'ünico∂é <{r}cc@mail.com>'),
        ('Bcc',    'zomügjå <{r}bcc@mail.com>'),
    ]

    headers = Headers()
    for key, value in default:
        headers.add(key, value.format(r=''))

    if resent:
        headers.add('Resent-Date')
        for key, value in default:
            headers.add('Resent-'+key, value.format(r='resent-'))
    return headers


def test_headers_sender(resent, headers):
    h = headers
    if resent:
        assert h.sender == 'resent-sender@mail.com'
        del h['Resent-Sender']
        assert h.sender == 'resent-from@mail.com'
    else:
        assert h.sender == 'sender@mail.com'
        del h['Sender']
        assert h.sender == 'from@mail.com'


def test_headers_receivers(resent, headers):
    h = headers
    if resent:
        assert h.receivers == [
            'resent-to@mail.com',
            'resent-cc@mail.com',
            'resent-bcc@mail.com',
        ]
    else:
        assert h.receivers == [
            'to@mail.com',
            'cc@mail.com',
            'bcc@mail.com'
        ]


def test_inject_headers(headers):
    mime = Message()
    inject_headers(mime, headers)
    keys = list(mime.keys())
    for key in keys:
        assert key not in ('Bcc', 'Resent-Bcc')
        assert mime[key] == encode_header(headers[key])
    assert keys


@pytest.mark.parametrize('key', ['key', 'key\'', '"key\\'])
@pytest.mark.parametrize('val', ['val', 'val\'', '"val\\'])
def test_generate_header(key, val):
    header = generate_header(key, {key: val})
    k, params = parse_header(header)
    assert unquote(k), params == (key, {key: val})


def test_encode_header():
    assert encode_header('abc') == 'abc'
    assert encode_header('é')   == '=?utf-8?b?w6k=?='
