from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

from datetime import datetime
import argparse

from twitter.models import Tweet

User = get_user_model()

class Command(BaseCommand):
    help = 'Emails a report of tweet counts by user'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--from_date',
            type=valid_date,
            help='The date to begin the tweet count (format YYYY-MM-DD)'
        )
        
        parser.add_argument(
            '--to_date',
            type=valid_date,
            help='The date to end the tweet count (format YYYY-MM-DD)'
        )
    
    def handle(self, *args, **options):
        # Get all tweets and filter them if filter arguments were specified
        all_tweets = Tweet.objects.all()
        if options['from_date']:
            all_tweets = all_tweets.filter(
                            created__gte=options['from_date']
                        )
        if options['to_date']:
            all_tweets = all_tweets.filter(
                            created__lte=options['to_date']
                        )
        
        # Process the tweets and create the report
        report_line = '{username}: {tweet_count}'
        report = []
        for user in User.objects.all():
            tweet_count = all_tweets.filter(user=user).count()
            report.append(
                report_line.format(
                    username=user.username,
                    tweet_count=tweet_count
                )
            )
        
        # Send the email
        send_mail(
            'Tweetsreport for Twitter Commands with Django', # subject
            '\n'.join(report), # body
            'noreply@twitter-commands.com',
            ['recipient@twitter-commands.com'],
            fail_silently=False,
        )


def valid_date(dt):
    '''
    Returns a datetime object from an input string formatted YYYY-MM-DD
    http://stackoverflow.com/a/25470943/3697120
    '''
    try:
        return datetime.strptime(dt, '%Y-%m-%d')
    except ValueError:
        # msg = 'Not a valid date: "{}"\nFormat date YYYY-MM-DD'.format(dt)
        msg = "Not a valid date: '{}'.".format(dt)
        raise argparse.ArgumentTypeError(msg)
