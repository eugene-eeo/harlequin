class Envelope(object):
    def __init__(self, enclosure, mail_from=None, rcpt_to=None):
        self.enclosure = enclosure
        self.mail_from = mail_from
        self.rcpt_to = rcpt_to

    @property
    def sender(self):
        return self.mail_from or self.enclosure.sender

    @property
    def receivers(self):
        return self.rcpt_to or self.enclosure.receivers

    def mime(self):
        return self.enclosure.mime()
