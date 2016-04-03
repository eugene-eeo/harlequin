import pytest
from harlequin.headers import UnicodeDict
from harlequin.utils import want_bytes, want_unicode


def test_unicodedict_init():
    u = UnicodeDict([
        (want_bytes('One'), want_bytes('1'))
    ])
    assert u[want_unicode('One')] == want_unicode('1')
