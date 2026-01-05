from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Comando para cargar datos iniciales desde apps.ready'

    def handle(self, *args, **options):
        print('Cargando datos iniciales de apps.ready')
