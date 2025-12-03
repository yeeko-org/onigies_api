# Create your models here.
from django.db import models
from pop.models import Sector


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


class AQuestion(models.Model):

    text = models.TextField()
    observable = models.ForeignKey(Observable, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pregunta: {self.text} ({self.observable.name})"

    class Meta:
        verbose_name = "Pregunta de institucionalización"
        verbose_name_plural = "Preguntas de institucionalización"


class PopulationQuestion(models.Model):

    text = models.TextField()
    observable = models.ForeignKey(Observable, on_delete=models.CASCADE)
    has_main_sectors = models.BooleanField(
        default=True, verbose_name="Tiene los sectores principales")
    others_sectors = models.ManyToManyField(Sector, blank=True)
    has_general_planning = models.BooleanField(
        default=False, verbose_name="Tiene la opción de planeación general")

    def __str__(self):
        return f"Pregunta población: {self.text} ({self.observable.name})"

    class Meta:
        verbose_name = "Pregunta de población"
        verbose_name_plural = "Preguntas de población"


class QuestionType(models.Model):
    # plan, body, population, special
    name = models.CharField(max_length=255)
    response_format = models.CharField(max_length=255)
    order = models.IntegerField(default=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tipo de pregunta"
        verbose_name_plural = "Tipos de preguntas"


class BQuestion(models.Model):

    observable = models.ForeignKey(Observable, on_delete=models.CASCADE)
    order = models.IntegerField(default=10)
    text = models.TextField()
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
    includes_academic = models.BooleanField(
        blank=True, null=True,
        verbose_name="Incluye entidades académicas")
    includes_admin = models.BooleanField(
        blank=True, null=True,
        verbose_name="Incluye dependencias administrativas")

    def __str__(self):
        return f"Pregunta cuerpo: {self.text} ({self.observable.name})"

    class Meta:
        verbose_name = "Pregunta de cuerpo"
        verbose_name_plural = "Preguntas de cuerpo"


class SpecialQuestion(models.Model):

    text = models.TextField()
    observable = models.ForeignKey(Observable, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pregunta especial: {self.text} ({self.observable.name})"

    class Meta:
        verbose_name = "Pregunta especial"
        verbose_name_plural = "Preguntas especiales"

