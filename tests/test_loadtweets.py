from django.core.management import call_command
from django.test import TestCase
from django.core.management.base import CommandError

from twitter.models import Tweet, User


class LoadTweetsTestCase(TestCase):

    def setUp(self):
        super(LoadTweetsTestCase, self).setUp()
        self.user = User.objects.create_user(
            username='rmotr_com', password='password123')

    def test_load_tweets_command(self):
        """Should import tweets from twitter API when given username is valid"""
        self.assertEqual(Tweet.objects.count(), 0)
        args = [self.user.username]
        call_command('loadtweets', *args)
        self.assertEqual(Tweet.objects.count(), 10)

    def test_load_tweets_command_invalid_username(self):
        """Should raise CommandError when given username does not exist"""
        self.assertEqual(Tweet.objects.count(), 0)
        args = ["INVALID"]
        with self.assertRaises(CommandError) as e:
            call_command('loadtweets', *args)
        self.assertEqual(e.exception.args[0], 'User "INVALID" does not exist')
        self.assertEqual(Tweet.objects.count(), 0)

    def test_load_tweets_command_count(self):
        """Should import the amount of tweets specified in the --count argument"""
        self.assertEqual(Tweet.objects.count(), 0)
        args = [self.user.username, "--count=20"]
        call_command('loadtweets', *args)
        self.assertEqual(Tweet.objects.count(), 20)
