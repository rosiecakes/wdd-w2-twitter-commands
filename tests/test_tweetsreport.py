from datetime import date
from django.test import TestCase
from django.core import mail
from django.core.management import call_command
from django.core.management.base import CommandError

from twitter.models import Tweet, User


class TweetsReportTestCase(TestCase):

    def setUp(self):
        super(TweetsReportTestCase, self).setUp()
        self.user = User.objects.create_user(
            username='User_ONE', password='password123')
        self.user_2 = User.objects.create_user(
            username='User_TWO', password='password123')
        self.tw_1 = Tweet.objects.create(user=self.user, content="User 1 - Tweet 1")
        self.tw_1.created = date(2016, 1, 1)
        self.tw_1.save()

        self.tw_2 = Tweet.objects.create(user=self.user, content="User 1 - Tweet 2")
        self.tw_2.created = date(2017, 1, 1)
        self.tw_2.save()

        self.tw_3 = Tweet.objects.create(user=self.user_2, content="User 2 - Tweet 1")
        self.tw_3.created = date(2015, 1, 1)
        self.tw_3.save()

        self.tw_4 = Tweet.objects.create(user=self.user_2, content="User 2 - Tweet 2")
        self.tw_4.created = date(2016, 1, 1)
        self.tw_4.save()

        self.tw_5 = Tweet.objects.create(user=self.user_2, content="User 2 - Tweet 3")
        self.tw_5.created = date(2017, 1, 1)
        self.tw_5.save()

    def test_load_tweets_report(self):
        """Should send by email a report with the amount of tweets from each user"""
        self.assertEqual(len(mail.outbox), 0)
        call_command('tweetsreport')
        self.assertEqual(len(mail.outbox), 1)
        email_report = mail.outbox[0].body
        self.assertTrue("User_ONE: 2" in email_report)
        self.assertTrue("User_TWO: 3" in email_report)

    def test_load_tweets_report_from_date(self):
        """Should only include tweets created after given from_date param"""
        self.assertEqual(len(mail.outbox), 0)
        args = ["--from_date=2016-6-6"]
        call_command('tweetsreport', *args)
        self.assertEqual(len(mail.outbox), 1)
        email_report = mail.outbox[0].body
        self.assertTrue("User_ONE: 1" in email_report)
        self.assertTrue("User_TWO: 1" in email_report)

    def test_load_tweets_report_to_date(self):
        """Should only include tweets created before given to_date param"""
        self.assertEqual(len(mail.outbox), 0)
        args = ["--to_date=2016-6-6"]
        call_command('tweetsreport', *args)
        self.assertEqual(len(mail.outbox), 1)
        email_report = mail.outbox[0].body
        self.assertTrue("User_ONE: 1" in email_report)
        self.assertTrue("User_TWO: 2" in email_report)

    def test_load_tweets_report_from_to_date(self):
        """Should only include tweets between given from_date and to_date params"""
        self.assertEqual(len(mail.outbox), 0)
        args = ["--from_date=2015-6-6", "--to_date=2016-6-6"]
        call_command('tweetsreport', *args)
        self.assertEqual(len(mail.outbox), 1)
        email_report = mail.outbox[0].body
        self.assertTrue("User_ONE: 1" in email_report)
        self.assertTrue("User_TWO: 1" in email_report)

    def test_load_tweets_report_invalid_date(self):
        """Should raise CommandError when given date in param is invalid"""
        args = ["--from_date=INVALID_FROM_DATE"]
        with self.assertRaises(CommandError) as e:
            call_command('tweetsreport', *args)
        self.assertEqual(e.exception.args[0],
                         "Not a valid date: 'INVALID_FROM_DATE'.")

        args = ["--to_date=INVALID_TO_DATE"]
        with self.assertRaises(CommandError) as e:
            call_command('tweetsreport', *args)
        self.assertEqual(e.exception.args[0],
                         "Not a valid date: 'INVALID_TO_DATE'.")
