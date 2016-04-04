"""
    harlequin.wire
    ~~~~~~~~~~~~~~

    Functions to deal with encoding and sending enclosure
    objects through sendmail or other protocols.

    :copyright: (c) 2016 Eeo Jun.
    :license: MIT, see LICENSE for details.
"""


def encode_address(addr):
    """
    Given a unicode address *addr*, return a (byte, on
    Python 2) string that is suitable to be passed as an
    argument to sendmail. It encodes the local-part using
    UTF-8 and the domain using IDNA.
    """
    try:
        addr = addr.encode('ascii')
    except UnicodeEncodeError:
        if '@' in addr:
            localpart, domain = addr.split('@', 1)
            addr = b'@'.join([
                localpart.encode('utf-8'),
                domain.encode('idna'),
            ])
        else:
            addr = addr.encode('utf-8')
    return addr.decode('utf-8')


def sendmail_args(enclosure_like):
    """
    Given an enclosure-like object (e.g.
    :class:`harlequin.envelope.Envelope` or one of the
    enclosures) *enclosure_like*, return a tuple
    in the form `(mail_from, rcpt_to, content)`
    suitable to be passed to the sendmail function.
    """
    sender = encode_address(enclosure_like.sender)
    receivers = [encode_address(k) for k in enclosure_like.receivers]
    return (
        sender,
        receivers,
        enclosure_like.mime().as_string()
        )
