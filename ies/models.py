from django.db import models


class Institution(models.Model):

    name = models.CharField(max_length=255, help_text="Nombre completo")
    logo = models.ImageField(upload_to="ies")
    acronym = models.CharField(max_length=50, help_text="Siglas únicas")
    year_start = models.IntegerField(default=2026)
    year_end = models.IntegerField(blank=True, null=True)
    is_public = models.BooleanField(
        blank=True, null=True, help_text="Es una institución pública?")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Institución de Educación Superior"
        verbose_name_plural = "Instituciones de Educación Superior"
