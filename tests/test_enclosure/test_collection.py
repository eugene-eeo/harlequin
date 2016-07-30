# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import pytest
from harlequin.utils import encode_header
from harlequin.enclosure import Collection, PlainText


@pytest.fixture(scope='module')
def parts():
    return [
        PlainText('∂', headers={'X-Key-1': 'one'}),
        PlainText('é', headers={'X-Key-2': 'two'}),
    ]


@pytest.fixture(scope='module')
def collection(parts):
    return Collection(parts, headers={
        'X-Key': 'value'
    })


def test_collection_mime_object(parts, collection):
    m = collection.mime_object()
    assert not m.defects

    real_mimes = m.get_payload()
    assert real_mimes

    for enclosure, actual in zip(parts, real_mimes):
        mime = enclosure.mime()
        assert mime.get_content_type() == actual.get_content_type()
        assert mime.get_payload() == actual.get_payload()


def test_collection_mime_headers(collection):
    m0 = collection.mime()
    m1, m2 = m0.get_payload()

    assert m0['X-Key'] == encode_header('value')
    assert m1['X-Key-1'] == encode_header('one')
    assert m2['X-Key-2'] == encode_header('two')


def test_collection_nested(parts, collection):
    c = Collection(parts + [collection])
    m = c.mime()

    assert not m.defects

    p1, p2, c1 = m.get_payload()
    p3, p4     = c1.get_payload()

    assert p1.get_payload() == parts[0].mime().get_payload()
    assert p2.get_payload() == parts[1].mime().get_payload()

    assert p3.get_payload() == parts[0].mime().get_payload()
    assert p4.get_payload() == parts[1].mime().get_payload()
