from django.utils.six import StringIO
from django.core.management import call_command
from django.test import TestCase
from django.core.management.base import CommandError

from twitter.models import Tweet, User


class LoadTweetsTestCase(TestCase):

    def setUp(self):
        super(LoadTweetsTestCase, self).setUp()
        self.user = User.objects.create_user(
            username='rmotr_com', password='password123')
        self.out = StringIO()

    def test_load_tweets_command(self):
        """Should import tweets from twitter API when given username is valid"""
        self.assertEqual(Tweet.objects.count(), 0)
        args = [self.user.username]
        call_command('loadtweets', stdout=self.out, *args)
        self.assertEqual(Tweet.objects.count(), 10)
        self.assertTrue(
            'Finished. 10 tweets have been imported.' in self.out.getvalue())
        for tweet in Tweet.objects.all():
            self.assertEqual(tweet.user, self.user)

    def test_load_tweets_command_count(self):
        """Should import the amount of tweets specified in the --count argument"""
        self.assertEqual(Tweet.objects.count(), 0)
        args = [self.user.username, "--count=20"]
        call_command('loadtweets', stdout=self.out, *args)
        self.assertEqual(Tweet.objects.count(), 20)
        self.assertTrue(
            'Finished. 20 tweets have been imported.' in self.out.getvalue())
        for tweet in Tweet.objects.all():
            self.assertEqual(tweet.user, self.user)

    def test_load_tweets_command_username_not_found(self):
        """Should raise CommandError when given username does not exist"""
        self.assertEqual(Tweet.objects.count(), 0)
        args = ["INVALID"]
        with self.assertRaises(CommandError) as e:
            call_command('loadtweets', stdout=self.out, *args)
        self.assertEqual(e.exception.args[0], 'User "INVALID" does not exist')
        self.assertEqual(Tweet.objects.count(), 0)

    def test_load_tweets_command_invalid_username(self):
        """Should raise TypeError when given username is not a string"""
        self.assertEqual(Tweet.objects.count(), 0)
        args = [123]
        with self.assertRaises(TypeError) as e:
            call_command('loadtweets', stdout=self.out, *args)
        self.assertEqual(e.exception.args[0], "'int' object is not subscriptable")
        self.assertEqual(Tweet.objects.count(), 0)

    def test_load_tweets_command_repeated_tweets(self):
        """Should not load tweets that already exists in the DB"""
        self.assertEqual(Tweet.objects.count(), 0)
        args = [self.user.username, "--count=20"]
        call_command('loadtweets', stdout=self.out, *args)
        self.assertTrue(
            'Finished. 20 tweets have been imported.' in self.out.getvalue())
        self.assertEqual(Tweet.objects.count(), 20)
        for tweet in Tweet.objects.all():
            self.assertEqual(tweet.user, self.user)
        args = [self.user.username, "--count=50"]
        call_command('loadtweets', stdout=self.out, *args)
        self.assertTrue(
            'Finished. 30 tweets have been imported.' in self.out.getvalue())
        self.assertEqual(Tweet.objects.count(), 50)
