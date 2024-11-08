from django.apps import AppConfig


class NutriscanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nutriscan'

    def ready(self):
        import nutriscan.signals  # Importa las señales
