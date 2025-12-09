from django.db import models

from indicator.models import Observable
from pop.models import Sector


class AQuestion(models.Model):

    text = models.TextField()
    observable = models.ForeignKey(Observable, on_delete=models.CASCADE)
    ponderation = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Pregunta: {self.text} ({self.observable.name})"

    class Meta:
        verbose_name = "Pregunta de institucionalización"
        verbose_name_plural = "Preguntas de institucionalización"


class AOption(models.Model):
    text = models.CharField(max_length=255)
    value = models.IntegerField()

    def __str__(self):
        return f"Opción de respuesta: {self.text} (Valor: {self.value})"

    class Meta:
        verbose_name = "Opción de respuesta de institucionalización"
        verbose_name_plural = "Opciones de respuesta de institucionalización"


class PopulationQuestion(models.Model):

    text = models.TextField()
    observable = models.ForeignKey(Observable, on_delete=models.CASCADE)
    has_main_sectors = models.BooleanField(
        default=True, verbose_name="Tiene los sectores principales")
    others_sectors = models.ManyToManyField(Sector, blank=True)
    has_general_planning = models.BooleanField(
        default=False, verbose_name="Tiene la opción de planeación general")
    ponderation = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00)

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
    ponderation = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00)
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
    ponderation = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Pregunta especial: {self.text} ({self.observable.name})"

    class Meta:
        verbose_name = "Pregunta especial"
        verbose_name_plural = "Preguntas especiales"
