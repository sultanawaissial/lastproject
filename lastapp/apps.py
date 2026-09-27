from django.apps import AppConfig

class LastappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lastapp'

    def ready(self):
        import lastapp.signals