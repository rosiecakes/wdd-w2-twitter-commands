from datetime import datetime
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError

from twitter.models import Tweet, User


def valid_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(date_str)
        raise CommandError(msg)


class Command(BaseCommand):
    help = 'Send by email a report with the amount of tweets for each user.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--from_date', default='',
            help="Filter tweets created after this date. i.e: --from_date='2016-4-21'",
        )
        parser.add_argument(
            '--to_date', default='',
            help="Filter tweets created before this date. i.e: --to_date='2016-4-21'",
        )

    def handle(self, *args, **options):
        from_date = valid_date(options['from_date']) if options['from_date'] else None
        to_date = valid_date(options['to_date']) if options['to_date'] else None

        tweets = Tweet.objects.all()
        if from_date:
            tweets = tweets.filter(created__gte=from_date)
        if to_date:
            tweets = tweets.filter(created__lte=to_date)

        report = {}
        for user in User.objects.all():
            report[user.username] = tweets.filter(user=user).count()

        report_template = "Twitter Clone report: "
        for user, count in report.items():
            report_template += "{}: {}, ".format(user, count)

        send_mail(
            'Tweets report per user.',
            report_template,
            'fake@email.com',
            ['fake_2@email.com'],
            fail_silently=False,
        )
