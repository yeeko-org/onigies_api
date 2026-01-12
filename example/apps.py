from django.apps import AppConfig
import sys

class ExampleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'example'

    def ready(self) -> None:
        from .initial_data import InitFeatures

        _ready = super().ready()
        if "migrate_initial_data" in sys.argv:
            print("Cargando datos iniciales de Ejemplo...")
            InitFeatures()
            print("Datos iniciales cargados.")
        return _ready
