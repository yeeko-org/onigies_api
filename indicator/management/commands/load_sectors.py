from django.core.management.base import BaseCommand
from django.db import transaction
from indicator.models import Sector

# class Sector(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)
#     needs_name = models.BooleanField(default=False)
#     order = models.IntegerField(default=0)
#     is_main = models.BooleanField(
#         default=True, verbose_name="Es sector principal")
#
#     def __unicode__(self):
#         return self.name


# Alumnado de nivel medio superior
# Alumnado de nivel licenciatura
# Alumnado de nivel posgrado
# Alumnado externo (de otras IES, intercambio o movilidad, servicio social, prácticas profesionales, voluntariado, etcétera)
# Posdoctorantes
# Personal académico de tiempo parcial / por horas / por asignatura (docencia, investigación)
# Personal académico de tiempo completo (docencia, investigación)
# Personal administrativo de base
# Personal administrativo de confianza
# Personal administrativo por honorarios
# Población externa (familias, proveedores, etcétera)
# Público en general (ex-alumnado y/o público asistente a actividades de extensión, artísticas, deportivas, etcétera).

class Command(BaseCommand):
    help = "Carga los datos iniciales de Sectores Poblacionales"

    def handle(self, *args, **kwargs):
        sectors = [
            {
                "name": "Titular de la IES",
                "description": "",
                "needs_name": False,
                "is_main": False,
            },
            {
                "name": "Máximo cuerpo colegiado de toda la IES",
                "description": "",
                "needs_name": False,
                "is_main": False,
            },
            {
                "name": "Autoridades y alto funcionariado",
                "description": "",
                "needs_name": False,
                "is_main": False,
            },
            {
                "name": "Alumnado de nivel medio superior",
                "description": "",
                "needs_name": False,
                "is_main": True,
            },
            {
                "name": "Alumnado de nivel licenciatura",
                "description": "",
                "needs_name": False,
                "is_main": True,
            },
            {
                "name": "Alumnado de nivel posgrado",
                "description": "",
                "needs_name": False,
                "is_main": True,
            },
            {
                "name": "Alumnado externo",
                "description": "De otras IES, intercambio o movilidad, servicio social, prácticas profesionales, voluntariado, etcétera",
                "needs_name": False,
                "is_main": True,
            },
            {
                "name": "Posdoctorantes",
                "description": "",
                "needs_name": False,
                "is_main": True,
            },
            {
                "name": "Personal académico de tiempo parcial / por horas / por asignatura",
                "description": "Docencia, investigación",
                "needs_name": False,
                "is_main": True,
            },
            {
                "name": "Personal académico de tiempo completo",
                "description": "Docencia, investigación",
                "needs_name": False,
                "is_main": True,
            },
            {
                "name": "Personal administrativo de base",
                "description": "",
                "needs_name": False,
                "is_main": True,
            },
            {
                "name": "Personal administrativo de confianza",
                "description": "",
                "needs_name": False,
                "is_main": True,
            },
            {
                "name": "Personal administrativo por honorarios",
                "description": "",
                "needs_name": False,
                "is_main": True,
            },
            {
                "name": "Población externa",
                "description": "Familias, proveedores, etcétera",
                "needs_name": False,
                "is_main": False,
            },
            {
                "name": "Público en general",
                "description": "Ex-alumnado y/o público asistente a actividades de extensión, artísticas, deportivas, etcétera",
                "needs_name": False,
                "is_main": False,
            },
        ]
        try:
            with transaction.atomic():
                for index, sector_data in enumerate(sectors):
                    Sector.objects.update_or_create(
                        name=sector_data["name"],
                        defaults={
                            "description": sector_data["description"],
                            "needs_name": sector_data["needs_name"],
                            "order": index + 1,
                            "is_main": sector_data["is_main"],
                        }
                    )
            self.stdout.write(self.style.SUCCESS("Sectores poblacionales cargados exitosamente."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error al cargar sectores poblacionales: {str(e)}"))
