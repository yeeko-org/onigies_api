from django.db import models


class Period(models.Model):
    year = models.IntegerField(primary_key=True, help_text="Año")
    published_date = models.DateField(
        help_text="Fecha de publicación del periodo", null=True, blank=True)


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

    is_deleted = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.group} - {self.public_name}"

    class Meta:
        ordering = ["group", "order"]
        verbose_name = "Status de control"
        verbose_name_plural = "Status de control (TODOS)"
