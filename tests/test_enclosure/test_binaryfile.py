# -*- coding: UTF-8 -*-
import pytest
from os.path import basename
from harlequin.enclosure import BinaryFile
from harlequin.utils import encode_header, generate_header


@pytest.fixture(params=['binary.gif', 'text.txt'], scope='module')
def filename(request):
    return 'tests/assets/%s' % request.param


@pytest.fixture(scope='module')
def binary(filename):
    return BinaryFile(filename)


def test_binaryfile_content(binary, filename):
    assert binary.content == open(filename, 'rb').read()


def test_binaryfile_mime(binary, filename):
    b = binary
    m = b.mime()
    is_gif = '.gif' in filename
    assert m['Content-Transfer-Encoding'] == encode_header('base64')
    assert m.get_content_type() == 'image/gif' if is_gif else 'text/plain'


def test_attachment_headers():
    b = BinaryFile(
        'tests/assets/binary.gif',
        headers={
            'Content-Type': 'arb',
            'X-Key': 'value',
        }
    )
    m = b.mime()
    assert m['Content-Type'] == encode_header('arb')
    assert m['X-Key'] == encode_header('value')
