# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import pytest
from smtplib import SMTP
from base64 import b64decode
from email.parser import Parser
from harlequin.enclosure import PlainText
from harlequin.headers import encode_header
from harlequin.wire import encode_address, sendmail_args
from harlequin.utils import want_bytes


@pytest.fixture(scope='module')
def enclosure():
    return PlainText(
        'content',
        headers={
            'Sender': 'sender@måil.com',
            'To':     'to@måîl.com',
        })


def test_encode_address():
    assert encode_address('üni') == 'üni'
    assert encode_address('uni@mail.com') == 'uni@mail.com'
    assert encode_address('üni@mail.com') == 'üni@mail.com'
    assert encode_address('üni@måil.com') == 'üni@xn--mil-ula.com'


def _test_mime(mime):
    assert not mime.defects
    assert mime['Sender'] == encode_header('sender@måil.com')
    assert mime['To'] == encode_header('to@måîl.com')
    assert b64decode(want_bytes(mime.get_payload())) == want_bytes('content')


def test_sendmail_args(enclosure):
    sender, receivers, string = sendmail_args(enclosure)
    assert sender == encode_address('sender@måil.com')
    assert receivers == [encode_address('to@måîl.com')]

    mime = Parser().parsestr(string)
    _test_mime(mime)


def test_sendmail_real(smtpserver, enclosure):
    host = smtpserver.addr[0]
    port = smtpserver.addr[1]
    s = SMTP(host, port)
    s.sendmail(*sendmail_args(enclosure))
    s.quit()

    assert len(smtpserver.outbox) == 1

    m = smtpserver.outbox[0]
    _test_mime(m)
