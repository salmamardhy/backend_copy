from django.apps import AppConfig


class NewappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'

    def ready(self):
        import account.signals
