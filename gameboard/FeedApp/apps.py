from django.apps import AppConfig


class FeedAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'FeedApp'

    def ready(self):
        import FeedApp.signals
