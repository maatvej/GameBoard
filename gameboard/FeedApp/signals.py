from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Reply
from django.conf import settings


@receiver(post_save, sender=Reply)
def notify_about_reply(sender, instance, **kwargs):
    if kwargs['created']:
        post_author_email = instance.post.author.email
        subject, from_email, to = 'New reply', settings.DEFAULT_FROM_EMAIL, post_author_email

        html_content = render_to_string(
            'reply_notify.html',
            {
                'text': f'{instance.body}',
                'link': f'{settings.SITE_URL}newsfeed/replies/{instance.pk}'
            }
        )

        msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@receiver(post_save, sender=Reply)
def reply_accepted(sender, instance, **kwargs):
    if instance.status:
        reply_author_email = instance.author.email
        subject, from_email, to = 'Your reply was accepted!', 'settings.DEFAULT_FROM_EMAIL', reply_author_email

        html_content = render_to_string(
            'reply_accepted.html',
            {
                'link': f'{settings.SITE_URL}newsfeed/replies/{instance.pk}'
            }
        )

        msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
