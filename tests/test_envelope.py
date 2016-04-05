# -*- coding: UTF-8 -*-
import pytest
from harlequin.envelope import Envelope
from harlequin.enclosure import Enclosure


@pytest.fixture(scope='module')
def enclosure():
    return Enclosure(headers=[
        ('Sender', 'sender@mail.com'),
        ('To',     'to@mail.com'),
    ])


@pytest.fixture(scope='module', params=[True, False])
def envelope(request, enclosure):
    env = Envelope(enclosure)
    if request.param:
        env.mail_from = 'mail_from@mail.com'
        env.rcpt_to   = ['rcpt_to@mail.com']
    return env


def test_envelope(envelope, enclosure):
    if not envelope.mail_from:
        assert envelope.sender == enclosure.sender
        assert envelope.receivers == enclosure.receivers
    else:
        assert envelope.sender == 'mail_from@mail.com'
        assert envelope.receivers == ['rcpt_to@mail.com']


def test_envelope_mime(envelope, enclosure):
    uniq = []
    enclosure.mime = lambda: uniq
    assert envelope.mime() is uniq


def test_envelope_empty_mail_from(enclosure):
    env = Envelope(enclosure, '')
    assert env.sender == ''


def test_envelope_empty_rcpt_to(enclosure):
    env = Envelope(enclosure, rcpt_to=[])
    assert env.receivers == []
