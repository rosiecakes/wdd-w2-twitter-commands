import tweepy
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from twitter.models import Tweet, User


class Command(BaseCommand):
    help = 'Load tweets from Twitter API into Twitter Clone for given username'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument(
            '--count', default=10,
            help='Amount of tweets that you want to load from API.',
        )

    def handle(self, *args, **options):
        auth = tweepy.OAuthHandler(settings.CONSUMER_KEY,
                                   settings.CONSUMER_SECRET)
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
            if not Tweet.objects.filter(id=tweet.id).exists():
                Tweet.objects.create(
                    id=tweet.id, user=user, content=tweet.text,
                    created=tweet.created_at
                )
