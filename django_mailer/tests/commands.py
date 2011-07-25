from django.core import mail
from django.core.management import call_command
from django_mailer import models
from django_mailer.tests.base import MailerTestCase
import datetime


class TestCommands(MailerTestCase):
    """
    A test case for management commands provided by django-mailer.

    """
    def test_send_mail(self):
        """
        The ``send_mail`` command initiates the sending of messages in the
        queue.

        """
        # No action is taken if there are no messages.
        call_command('send_mail', verbosity='0')
        # Any (non-deferred) queued messages will be sent.
        self.queue_message()
        self.queue_message()
        self.queue_message(subject='deferred')
        models.QueuedMessage.objects\
                    .filter(message__subject__startswith='deferred')\
                    .update(deferred=datetime.datetime.now())
        queued_messages = models.QueuedMessage.objects.all()
        self.assertEqual(queued_messages.count(), 3)
        self.assertEqual(len(mail.outbox), 0)
        call_command('send_mail', verbosity='0')
        self.assertEqual(queued_messages.count(), 1)
        self.assertEqual(len(mail.outbox), 2)

    def test_retry_deferred(self):
        """
        The ``retry_deferred`` command places deferred messages back in the
        queue.

        """
        self.queue_message()
        self.queue_message(subject='deferred')
        self.queue_message(subject='deferred 2')
        self.queue_message(subject='deferred 3')
        models.QueuedMessage.objects\
                    .filter(message__subject__startswith='deferred')\
                    .update(deferred=datetime.datetime.now())
        non_deferred_messages = models.QueuedMessage.objects.non_deferred()
        # Deferred messages are returned to the queue (nothing is sent).
        self.assertEqual(non_deferred_messages.count(), 1)
        call_command('retry_deferred', verbosity='0')
        self.assertEqual(non_deferred_messages.count(), 4)
        self.assertEqual(len(mail.outbox), 0)
        # Check the --max-retries logic.
        models.QueuedMessage.objects\
                    .filter(message__subject='deferred')\
                    .update(deferred=datetime.datetime.now(), retries=2)
        models.QueuedMessage.objects\
                    .filter(message__subject='deferred 2')\
                    .update(deferred=datetime.datetime.now(), retries=3)
        models.QueuedMessage.objects\
                    .filter(message__subject='deferred 3')\
                    .update(deferred=datetime.datetime.now(), retries=4)
        self.assertEqual(non_deferred_messages.count(), 1)
        call_command('retry_deferred', verbosity='0', max_retries=3)
        self.assertEqual(non_deferred_messages.count(), 3)

    def test_idn_addresses(self):
        """
        To and from addresses should be encoded using ``idna`` before being
        passed to the smtp server
        """

        # This is a valid IDN address, and will pass Django's email address
        # validation.
        from_email = u'someone@h\u200botmail.co.u\u200bk'
        to_email = u'someone_else@h\u200botmail.co.u\u200bk'
        self.queue_message(from_email=from_email, recipient_list=[to_email])
        call_command('send_mail', verbosity='0')
        self.assertEqual(1, len(mail.outbox))
        m = mail.outbox[0]
        self.assertEqual(from_email.encode('idna'), m.from_email)
        self.assertEqual([to_email.encode('idna')], m.to)
