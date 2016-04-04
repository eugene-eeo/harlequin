# -*- coding: UTF-8 -*-
import pytest
from smtplib import SMTP
from base64 import b64decode
from email.parser import Parser
from harlequin.enclosure import PlainText
from harlequin.wire import encode_address, sendmail_args
from harlequin.utils import want_bytes, encode_header


@pytest.fixture(scope='module')
def enclosure():
    return PlainText(
        'content',
        headers={
            'Sender': 'sender@måil.com',
            'To':     'to@måîl.com',
        })


def test_encode_address():
    assert encode_address(u'üni') == u'üni'
    assert encode_address(u'uni@mail.com') == u'uni@mail.com'
    assert encode_address(u'üni@mail.com') == u'üni@mail.com'
    assert encode_address(u'üni@måil.com') == u'üni@xn--mil-ula.com'


def test_sendmail_args(enclosure):
    sender, receivers, string = sendmail_args(enclosure)
    assert sender == encode_address(u'sender@måil.com')
    assert receivers == [encode_address(u'to@måîl.com')]

    mime = Parser().parsestr(string)
    assert mime['Sender'] == encode_header(u'sender@måil.com')
    assert mime['To'] == encode_header(u'to@måîl.com')
    assert b64decode(mime.get_payload()) == want_bytes('content')


def test_sendmail_real(smtpserver, enclosure):
    host = smtpserver.addr[0]
    port = smtpserver.addr[1]
    s = SMTP(host, port)
    s.sendmail(*sendmail_args(enclosure))
    s.quit()

    assert len(smtpserver.outbox) == 1

    m = smtpserver.outbox[0]
    assert m['Sender'] == encode_header(u'sender@måil.com')
    assert m['To']     == encode_header(u'to@måîl.com')
    assert b64decode(m.get_payload()) == want_bytes('content')
