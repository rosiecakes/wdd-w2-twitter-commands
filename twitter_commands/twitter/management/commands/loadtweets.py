import tweepy
from django.core.management.base import BaseCommand, CommandError

from twitter.models import Tweet, User


consumer_key = "hyo6w5ew77IVnk844ECSJCAgw"
consumer_secret = "CshiCMqkDCVvg8lRtdqPxlDoleOUTAw7fdhHCojTEzkd3TaMVN"


class Command(BaseCommand):
    help = 'Load tweets from Twitter API into Twitter Clone for given username'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument(
            '--count', default=10,
            help='Amount of tweets that you want to load from API.',
        )

    def handle(self, *args, **options):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        api = tweepy.API(auth)
        username = options['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if not user:
            raise CommandError('User "{}" does not exist'.format(username))

        tweets = api.user_timeline(options['username'], count=options['count'])
        for tweet in tweets:
            Tweet.objects.create(
                user=user, content=tweet.text, created=tweet.created_at
            )
