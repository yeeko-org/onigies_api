from django.contrib.auth.models import AbstractUser
from django.db import models


class Institution(models.Model):

    name = models.CharField(max_length=255, help_text="Nombre completo")
    logo = models.ImageField(upload_to="ies", blank=True, null=True)
    acronym = models.CharField(max_length=50, help_text="Siglas únicas")
    year_start = models.IntegerField(blank=True, null=True)
    year_end = models.IntegerField(blank=True, null=True)
    is_public = models.BooleanField(
        blank=True, null=True, help_text="Es una institución pública?")
    # is_testing = models.BooleanField(
    #     default=False, help_text="¿Es una institución de prueba?")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        periods = Period.objects.all()
        for period in periods:
            self.surveys.get_or_create(period=period)
            self.packages.get_or_create(period=period)


    class Meta:
        verbose_name = "Institución de Educación Superior"
        verbose_name_plural = "Instituciones de Educación Superior"

# init_institutions = [
#     {
#         "name": "Instituto Politécnico Nacional",
#         "acronym": "IPN",
#         "is_public": True,
#     },
#     {
#         "name": "Universidad Nacional Autónoma de México",
#         "acronym": "UNAM",
#         "is_public": True,
#     },
#     {
#         "name": "Tecnológico de Monterrey",
#         "acronym": "ITESM",
#         "is_public": False,
#     },
# ]

class User(AbstractUser):
    phone = models.CharField(max_length=100, blank=True)
    full_editor = models.BooleanField(
        default=False, verbose_name='Es capturista',
        help_text='Puede agregar notas, comentarios a los registros,'
                  'pero no tiene todos los permisos')
    mini_editor = models.BooleanField(
        default=False, verbose_name='Servicio social',
        help_text='Puede modificar ubicaciones y otros detalles')
    institution = models.ForeignKey(
        Institution, on_delete=models.CASCADE, blank=True, null=True,
        related_name='users')

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        if self.first_name or self.last_name:
            return f"{self.first_name or self.last_name}"
        return self.username or self.email

    @property
    def is_full_editor(self):
        if self.is_anonymous:
            return False
        return self.is_superuser or self.is_staff or self.full_editor

    @property
    def is_admin(self):
        if self.is_anonymous:
            return False
        return self.is_superuser or self.is_staff


class Period(models.Model):
    year = models.IntegerField(primary_key=True, help_text="Año")
    explanation = models.TextField(
        verbose_name="Recuento de fechas", blank=True, null=True)
    good_practices_published = models.BooleanField(
        verbose_name="Buenas prácticas publicadas", default=False)
    # published_date = models.DateField(
    #     null=True, blank=True,
    #     verbose_name="Fecha de publicación del periodo")
    results_published = models.BooleanField(
        verbose_name="Resultados publicados", default=False)

    def __str__(self):
        return str(self.year)

    class Meta:
        verbose_name = "Periodo"
        verbose_name_plural = "Periodos"


GROUP_CHOICES = [
    ("register", "Registro"),
    ("validation", "Validación"),
]
ROLE_CHOICES = [
    ("validator", "Validador"),
    ("ies", "Institución"),
]


class StatusControl(models.Model):
    name = models.CharField(max_length=120, primary_key=True)
    group = models.CharField(
        max_length=10, choices=GROUP_CHOICES,
        verbose_name="grupo de status", default="petition")
    public_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(
        max_length=30, blank=True, null=True,
        help_text="https://vuetifyjs.com/en/styles/colors/")
    icon = models.CharField(
        max_length=40, blank=True, null=True,
        help_text="https://fonts.google.com/icons")
    order = models.IntegerField(default=4)

    is_final = models.BooleanField(default=False)

    send_ies = models.BooleanField(default=False)
    strict_ies = models.BooleanField(default=False)
    send_admin = models.BooleanField(default=False)
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES,
        verbose_name="rol asociado", default="ies")
    # is_public = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.group} - {self.public_name}"

    class Meta:
        ordering = ["group", "order"]
        verbose_name = "Status de control"
        verbose_name_plural = "Status de control (TODOS)"
