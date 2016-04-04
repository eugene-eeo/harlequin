harlequin
=========

.. image:: https://travis-ci.org/eugene-eeo/harlequin.svg?branch=master
    :target: https://travis-ci.org/eugene-eeo/harlequin

A composable and sane alternative to MIME-handling for Python.
The name comes from mime, which is synonymous with harlequin.
Harlequin only handles email-creation. Includes goodies like:

- A saner headers system
- Encoding functions and code you don't want to write
- ``Resent-*`` aware headers and RFC compliance
- Automatic sender/receiver address extraction
- Unicode aware headers and classes
- Python 3 readiness

.. code-block:: python

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
