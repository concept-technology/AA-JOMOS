from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from book_store.models import EmailSubscription
from django.conf import settings

class Command(BaseCommand):
    help = 'Send emails to all active subscribers'

    def handle(self, *args, **kwargs):
        subscribers = EmailSubscription.objects.all()  # You can filter if you want to send only to active subscribers
        email_list = [subscriber.email for subscriber in subscribers]

        if email_list:
            send_mail(
                subject='Our Latest News',
                message='Here is the latest news from our eCommerce store.',
                from_email='',
                recipient_list=email_list,
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully sent emails to {len(email_list)} subscribers'))
        else:
            self.stdout.write(self.style.WARNING('No subscribers found.'))
