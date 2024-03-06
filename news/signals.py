from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User

from .models import News

@receiver(post_save, sender=News)
def send_notification_email(sender, instance, **kwargs):
    subject = 'New post published'
    message = f'News "{instance.title}" was published!.'
    from_email = 'mirafzaaal2609@gmail.com'
    user_emails = User.objects.values_list('email', flat=True)

    for email in user_emails:
        send_mail(subject, message, from_email, [email], fail_silently=True)
