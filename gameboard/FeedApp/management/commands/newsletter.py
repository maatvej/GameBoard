from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings


class Command(BaseCommand):
    help = 'Подсказка вашей команды'

    def handle(self, *args, **options):
        message = input("Введите сообщение для новостной рассылки: ")
        for user in User.objects.all():
            email = user.email
            send_mail(
                "Новостная рассылка!",
                f'{message}',
                f'{settings.DEFAULT_FROM_EMAIL}',
                [email]
            )
