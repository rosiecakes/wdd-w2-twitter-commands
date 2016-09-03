from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

import tweepy

from django.conf import settings
from twitter.models import Tweet


User = get_user_model()

class Command(BaseCommand):
    help = 'Fetches tweets from Twitter API and loads them into local db'
     
    def add_arguments(self, parser):
        # Positional - this is the user we want to get the tweets from
        parser.add_argument('username', type=str)
        
        # Named, optional
        # https://docs.djangoproject.com/en/1.9/howto/custom-management-commands/#accepting-optional-arguments
        parser.add_argument(
            '--count',
            type=int,
            default=10,  # see line 22, test_loadtweets; still need to set max to 200
            help='The number of tweets to be loaded (default 10)'
        )
    
    def handle(self, *args, **options):
        # Authenticate
        # https://www.digitalocean.com/community/tutorials/how-to-authenticate-a-python-application-with-twitter-using-tweepy-on-ubuntu-14-04
        auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        
        # Get the user to be updated
        username = options['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError('User "{}" does not exist'.format(username))
        
        # Query the Twitter API for tweets by the user
        # http://tweepy.readthedocs.io/en/v3.5.0/code_snippet.html
        count = 0
        for tweet in tweepy.Cursor(api.user_timeline, id=user).items(options['count']):
            loaded_tweet, created = Tweet.objects.get_or_create(
                user=user, 
                content=tweet.text, 
                created=tweet.created_at)
            if created: 
              loaded_tweet.created = tweet.created_at
              loaded_tweet.save()
              count += 1
        
        self.stdout.write("Finished. {} tweets have been imported.".format(count))
        
        print("User:", username)
        print("Count:", count)