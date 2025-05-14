from django.apps import AppConfig


class HesabatyWebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hesabaty_web'

    def ready(self):
        import hesabaty_web.signals