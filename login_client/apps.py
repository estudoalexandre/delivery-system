from django.apps import AppConfig


class LoginClientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'login_client'


class LoginClientConfig(AppConfig):
    name = 'login_client'
    def ready(self):
        import login_client.signals