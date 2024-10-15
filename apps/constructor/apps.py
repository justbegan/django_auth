from django.apps import AppConfig


class ConstructorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.constructor'
    def ready(self):
        import apps.constructor.signals
