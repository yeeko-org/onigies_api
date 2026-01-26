from django.apps import AppConfig
import sys

class IesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ies'


    def ready(self) -> None:
        from ies.initial_data import InitStatus, InitPeriod
        _ready = super().ready()
        if 'migrate_initial_data' in sys.argv:
            print('Cargando datos iniciales de work_flux...')
            InitStatus()
            InitPeriod()
            print('Datos iniciales cargados.')
        return _ready
