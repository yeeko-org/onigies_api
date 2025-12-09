# Create your models here.
from django.db import models


class Axis(models.Model):
    number = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=55, blank=True, null=True)
    logo = models.ImageField(blob=True, upload_to='axis_logos/')
    color = models.CharField(max_length=55)
    hex_color = models.CharField(max_length=7, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Materia (Axis)"
        verbose_name_plural = "Materias (Axes)"


class Component(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    axis = models.ForeignKey(Axis, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.axis.name})"


class Observable(models.Model):

    number = models.DecimalField(max_digits=4, decimal_places=2)
    name = models.CharField(max_length=255)
    init_question = models.TextField(blank=True, null=True)
    a_main_question = models.TextField(
        blank=True, null=True,
        verbose_name="Pregunta institucionalización")
    a_main_subtitle = models.TextField(
        blank=True, null=True,
        verbose_name="Subtítulo institucionalización")
    description = models.TextField(blank=True, null=True)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.component.name})"

    class Meta:
        verbose_name = "Observable"
        verbose_name_plural = "Observables"


