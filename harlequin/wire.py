def encode_address(addr, encoding='utf-8'):
    try:
        addr = addr.encode('ascii')
    except UnicodeEncodeError:
        if '@' in addr:
            localpart, domain = addr.split('@', 1)
            addr = b'@'.join([
                localpart.encode(encoding),
                domain.encode('idna'),
            ])
        else:
            addr = addr.encode(encoding)
    return addr


def sendmail_args(enclosure_like):
    sender = encode_address(enclosure_like.sender)
    receivers = [encode_address(k) for k in enclosure_like.receivers]
    return (
        sender,
        receivers,
        enclosure_like.mime().as_string()
        )
