# -*- coding: UTF-8 -*-
import pytest
from os.path import basename
from harlequin.enclosure import Attachment
from harlequin.utils import encode_header, generate_header


@pytest.fixture(params=['binary.gif', 'text.txt'], scope='module')
def attachment(request):
    return Attachment(
        'tests/assets/%s' % request.param
    )


def test_attachment_content(attachment):
    a = attachment
    assert a.content == open(a.path, 'rb').read()


def test_attachment_mime(attachment):
    a = attachment
    m = a.mime()
    is_gif = '.gif' in attachment.path
    assert m['Content-Transfer-Encoding'] == encode_header('base64')
    assert m.get_content_type() == 'image/gif' if is_gif else 'text/plain'
    assert m['Content-Disposition'] == generate_header(
        'attachment',
        {'filename': basename(a.path)}
    )


def test_attachment_headers(attachment):
    a = Attachment(
        'tests/assets/binary.gif',
        headers={
            'Content-Type': 'arb',
            'X-Key': 'value',
        }
    )
    m = a.mime()
    assert m['Content-Type'] == encode_header('arb')
    assert m['X-Key'] == encode_header('value')
