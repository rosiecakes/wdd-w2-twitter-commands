from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

from twitter.models import Tweet

User = get_user_model()

class Command(BaseCommand):
    help = 'Fetches tweets from Twitter API and loads them into local db'
    
    def add_arguments(self, parser):
        # Positional
        parser.add_argument('username', type=str)
        
        # Named, optional
        # https://docs.djangoproject.com/en/1.9/howto/custom-management-commands/#accepting-optional-arguments
        parser.add_argument(
            '--count',
            type=int,
            default=200,
            help='The number of tweets to be loaded (default 200)'
        )
    
    def handle(self, *args, **options):
        # Get the user to be updated
        username = options['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError('User "{}" does not exist locally'.format(username))
        
        # Query the Twitter API for tweets by the user
        count = options['count']
        
        print("User:", username)
        print("Count:", count)