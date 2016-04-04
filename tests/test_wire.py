import pytest
from base64 import b64decode
from email.parser import Parser
from harlequin.enclosure import PlainText
from harlequin.wire import encode_address, sendmail_args
from harlequin.utils import want_bytes, encode_header


def test_encode_address():
    assert encode_address('uni@mail.com') == want_bytes('uni@mail.com')
    assert encode_address('üni@mail.com') == want_bytes('üni@mail.com')
    assert encode_address('üni@måil.com') == \
            want_bytes('üni') \
            + want_bytes('@') \
            + want_bytes('måil.com', charset='idna')


def test_sendmail_args():
    sender, receivers, string = sendmail_args(PlainText(
        'content',
        headers={
            'Sender': 'sender@mail.com',
            'To':     'to@mail.com',
        }))
    assert sender == encode_address(u'sender@mail.com')
    assert receivers == [encode_address(u'to@mail.com')]

    mime = Parser().parsestr(string)
    assert mime['Sender'] == encode_header(u'sender@mail.com')
    assert mime['To'] == encode_header(u'to@mail.com')
    assert b64decode(mime.get_payload()) == want_bytes('content')
