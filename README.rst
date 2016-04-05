Harlequin: Sane MIME Handling
=============================

.. image:: https://travis-ci.org/eugene-eeo/harlequin.svg?branch=master
    :target: https://travis-ci.org/eugene-eeo/harlequin

.. image:: https://ci.appveyor.com/api/projects/status/rda1s4gghx6c6wsr/branch/master?svg=true
    :target: https://ci.appveyor.com/project/eugene-eeo/harlequin

An MIT-licensed, composable and sane alternative to MIME-handling
for Python. Inspired by Werkzeug, Harlequin handles inconveniences
associated with internalisation and encoding for you::

    >>> from harlequin.enclosure import PlainText
    >>> from harlequin.wire import sendmail_args
    >>> mail_from, rcpt_to, content = sendmail_args(PlainText(
      content='ünicode-awåré',
      headers={
        'Sender': 'Name <name@îdna-aé.org>',
        'To':     'ünic <unic@idna-ae.org>',
      }
    ))

    >>> mail_from
    'name@xn--dna-a-fsa3a.org'
    >>> rcpt_to
    ['unic@idna-ae.org']
    >>> content
    # Content-Type: ...

Features
--------

- A saner headers system
- Encoding functions and code you don't want to write
- ``Resent-*`` aware headers and RFC compliance
- Automatic sender/receiver address extraction
- Unicode aware headers and classes
- Python 3 readiness
