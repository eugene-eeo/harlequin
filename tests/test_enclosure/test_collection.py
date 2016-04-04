import pytest
from harlequin.utils import encode_header
from harlequin.enclosure import Collection, PlainText


@pytest.fixture(scope='module')
def parts():
    return [
        PlainText(u'∂', headers={'X-Key-1': 'one'}),
        PlainText(u'é', headers={'X-Key-2': 'two'}),
    ]


@pytest.fixture(scope='module')
def collection(parts):
    return Collection(parts, headers={
        'X-Key': 'value'
    })


def test_collection_mime_object(parts, collection):
    m = collection.mime_object()
    assert not m.defects

    mimes = m.get_payload()
    assert mimes

    for idx, mime in enumerate(mimes):
        assert mime.get_content_type() == 'text/plain'
        assert mime.get_payload() == parts[idx].mime().get_payload()


def test_collection_mime_headers(parts, collection):
    m0 = collection.mime()
    m1, m2 = m0.get_payload()

    assert m0['X-Key'] == encode_header(u'value')
    assert m1['X-Key-1'] == encode_header(u'one')
    assert m2['X-Key-2'] == encode_header(u'two')


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
