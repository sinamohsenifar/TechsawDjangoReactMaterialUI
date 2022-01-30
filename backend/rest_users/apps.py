from django.apps import AppConfig


class RestUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rest_users'

    def ready(self):
        import rest_users.signals