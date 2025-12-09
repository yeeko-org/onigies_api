from django.db import models

from indicator.models import Observable
from question.models import (
    PopulationQuestion, AQuestion, AOption, BQuestion)
from ies.models import Institution
from workflux.models import Period, StatusControl
from pop.models import Sector
from profile_auth.models import User


class Survey(models.Model):

    institution = models.ForeignKey(
        Institution, on_delete=models.CASCADE, related_name='surveys')
    period = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='surveys')
    academic_instances = models.IntegerField(
        verbose_name='Instancias académicas')
    admin_instances = models.IntegerField(
        verbose_name='Instancias administrativas')
    sectors = models.ManyToManyField(
        Sector, related_name='surveys',
        verbose_name='Sectores atendidos')
    plans_media = models.IntegerField(
        verbose_name='Planes a nivel medio superior')
    plans_superior = models.IntegerField(
        verbose_name='Planes a nivel superior')
    plans_postgraduate = models.IntegerField(
        verbose_name='Planes a nivel posgrado')

    def __str__(self):
        return f"Survey for {self.institution.name} during {self.period.name}"

    class Meta:
        unique_together = ('institution', 'period')
        verbose_name = 'Conjunto de respuestas IES-Año'
        verbose_name_plural = 'Conjuntos de respuestas IES-Año'


OBSERVABLE_OPTIONS = (
    ('sí', 'Sí'),
    ('no', 'No'),
    # ('partial', 'Parcialmente'),
)


class PopulationQuantity(models.Model):
    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name='population_quantities')
    sector = models.ForeignKey(
        Sector, on_delete=models.CASCADE, related_name='population_quantities')
    no_apply = models.BooleanField(default=False, verbose_name="No Aplica")
    name = models.CharField(max_length=255, verbose_name='Nombre del sector')
    number_men = models.PositiveIntegerField(
        verbose_name='Número de hombres')
    number_women = models.PositiveIntegerField(
        verbose_name='Número de mujeres')

    def __str__(self):
        return f"{self.sector.name}: {self.number_men} hombres, {self.number_women} mujeres"

    class Meta:
        verbose_name = 'Cantidad de población por sector'
        verbose_name_plural = 'Cantidades de población por sector'


class ObservableResponse(models.Model):

    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name='observable_responses')
    observable = models.ForeignKey(
        Observable, on_delete=models.CASCADE, related_name='responses')
    value = models.CharField(
        max_length=10, choices=OBSERVABLE_OPTIONS,
        verbose_name='Valor de la respuesta')

    def __str__(self):
        return f"Response to '{self.observable.name}'"

    class Meta:
        verbose_name = 'Respuesta observable'
        verbose_name_plural = 'Respuestas observables'


class PopulationResponse(models.Model):
    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name='population_responses')
    question = models.ForeignKey(
        PopulationQuestion, on_delete=models.CASCADE, related_name='responses')
    not_focalized = models.BooleanField(
        verbose_name='No focalizado en sectores específicos',
        default=False)
    sectors = models.ManyToManyField(
        Sector, related_name='population_responses', blank=True)

    def __str__(self):
        return f"Response to '{self.question.text}'"

    class Meta:
        verbose_name = 'Respuesta de población'
        verbose_name_plural = 'Respuestas de población'


class AResponse(models.Model):
    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name='a_question_responses')
    question = models.ForeignKey(
        AQuestion, on_delete=models.CASCADE, related_name='responses')
    selected_option = models.ForeignKey(
        AOption, on_delete=models.CASCADE,
        related_name='a_responses')

    def __str__(self):
        return f"Response to '{self.question.text}'"

    class Meta:
        verbose_name = 'Respuesta a pregunta A'
        verbose_name_plural = 'Respuestas a preguntas A'


class BResponse(models.Model):
    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name='b_question_responses')
    question = models.ForeignKey(
        BQuestion, on_delete=models.CASCADE, related_name='responses')

    def __str__(self):
        return f"Response to '{self.question.text}'"

    class Meta:
        verbose_name = 'Respuesta a pregunta B'
        verbose_name_plural = 'Respuestas a preguntas B'


    status_validation = models.ForeignKey(
        StatusControl, on_delete=models.CASCADE,
        related_name='a_responses')


class GenericResponse(models.Model):
    a_response = models.ForeignKey(
        AResponse, on_delete=models.CASCADE, related_name='generic_responses')
    b_response = models.ForeignKey(
        BResponse, on_delete=models.CASCADE, related_name='generic_responses')
    population_response = models.ForeignKey(
        PopulationResponse, on_delete=models.CASCADE,
        related_name='generic_responses')
    value = models.TextField(verbose_name='Valor de la respuesta')
    status_validation = models.ForeignKey(
        StatusControl, on_delete=models.CASCADE,
        related_name='generic_responses')

    def __str__(self):
        return f"Generic Response ID {self.id}"

    class Meta:
        verbose_name = 'Respuesta genérica'
        verbose_name_plural = 'Respuestas genéricas'


class Attachment(models.Model):
    generic_response = models.ForeignKey(
        GenericResponse, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='comment_attachments/')

    def __str__(self):
        return f"Attachment for response ID {self.generic_response.id}"

    class Meta:
        verbose_name = 'Adjunto de comentario'
        verbose_name_plural = 'Adjuntos de comentarios'


class Comment(models.Model):
    # a_response = models.ForeignKey(
    #     AResponse, on_delete=models.CASCADE,
    #     blank=True, null=True, related_name='comments')
    # population_response = models.ForeignKey(
    #     PopulationResponse, on_delete=models.CASCADE,
    #     blank=True, null=True, related_name='comments')
    generic_response = models.ForeignKey(
        GenericResponse, on_delete=models.CASCADE,
        related_name='comments')
    text = models.TextField(verbose_name='Texto del comentario')
    status_validation = models.ForeignKey(
        StatusControl, on_delete=models.CASCADE,
        related_name='a_responses')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')

    # def __str__(self):
    #     return f"Comentario by {self.user.username} on response ID {self.a_response.id}"

    class Meta:
        verbose_name = 'Comentario de encuesta'
        verbose_name_plural = 'Comentarios de encuestas'


