"""
    harlequin.envelope
    ~~~~~~~~~~~~~~~~~~

    Implements the Envelope class.

    :copyright: (c) 2016 Eeo Jun.
    :license: MIT, see LICENSE for details.
"""


class Envelope(object):
    """
    An Envelope is a wrapper around an enclosure
    that provides a way to hide the "original"
    sender/receivers. If you send an envelope,
    then the message is sent from sender (*mail_from*)
    to the receivers (*rcpt_to*), regardless of
    the headers of the enclosure.

    :param enclosure: Enclosure to wrap around.
    :param mail_from: Optional email address of sender.
    :param rcpt_to: Optional list of email address(es)
        of receivers.
    """

    def __init__(self, enclosure, mail_from=None, rcpt_to=None):
        self.enclosure = enclosure
        self.mail_from = mail_from
        self.rcpt_to = rcpt_to

    @property
    def sender(self):
        """
        Returns the address if specified in
        ``mail_from``, else returns the `sender`
        property of the enclosure.
        """
        if self.mail_from is None:
            return self.enclosure.sender
        return self.mail_from

    @property
    def receivers(self):
        """
        Returns the addresses if specified in
        ``rcpt_to``, else returns the `receivers`
        property of the enclosure.
        """
        if self.rcpt_to is None:
            return self.enclosure.receivers
        return self.rcpt_to

    def mime(self):
        """
        Returns the result of calling the
        ``mime`` method of the enclosure.
        """
        return self.enclosure.mime()
