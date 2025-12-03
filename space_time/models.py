from django.db import models


class Period(models.Model):
    year = models.IntegerField(primary_key=True, help_text="Año")
    published_date = models.DateField(
        help_text="Fecha de publicación del periodo", null=True, blank=True)
