import pytest
from cgi import parse_header
from harlequin.headers import UnicodeDict, Headers
from harlequin.utils import want_bytes


def test_unicodedict_init():
    u = UnicodeDict([
        (want_bytes('One'), want_bytes('1'))
    ])
    assert u[u'One'] == u'1'


def test_unicodedict_setitem():
    u = UnicodeDict()
    u[want_bytes('One')] = want_bytes('1')
    assert u[u'One'] == u'1'


def test_headers_add():
    value, params = 'Value', {'param': 'value'}
    h = Headers()
    h.add('Key', value, **params)
    assert parse_header(h[u'Key']) == (value, params)


def test_headers_resent():
    h = Headers()
    h.add('Resent-Date')
    assert h.resent


def test_headers_sender():
    h = Headers()
    h.add('From', 'from@mail.com')
    assert h.sender == 'from@mail.com'

    h.add('Sender', 'Sender <sender@mail.com>')
    assert h.sender == 'sender@mail.com'
