from django.apps import AppConfig


class UserappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userApp'
    verbose_name = "Пользователи"

    def ready(self):
        import userApp.signals
