from django.db import models

from indicator.models import Observable, Sector
from ies.models import User, StatusControl
from question.models import (
    QuestionGroup, ReachQuestion, AQuestion, AOption, PlanQuestion,
    BQuestion, SpecialQuestion)
from survey.models import Survey


class ObservableResponse(models.Model):

    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name='observable_responses')
    observable = models.ForeignKey(
        Observable, on_delete=models.CASCADE, related_name='responses')
    status_validation = models.ForeignKey(
        StatusControl, on_delete=models.CASCADE)
    value = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return f"Response to '{self.observable.name}'"

    class Meta:
        verbose_name = 'Respuesta observable'
        verbose_name_plural = 'Respuestas observables'


class Comment(models.Model):
    observable_response = models.ForeignKey(
        ObservableResponse, on_delete=models.CASCADE, related_name='comments')
    question_group = models.ForeignKey(
        QuestionGroup, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Texto del comentario')
    status_validation = models.ForeignKey(
        StatusControl, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on '{self.observable_response.observable.name}'"

    class Meta:
        verbose_name = 'Comentario de encuesta'
        verbose_name_plural = 'Comentarios de encuestas'


class ReachResponse(models.Model):
    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name='reach_responses')
    question = models.ForeignKey(
        ReachQuestion, on_delete=models.CASCADE, related_name='responses')
    not_focalized = models.BooleanField(
        verbose_name='No focalizado en sectores específicos',
        default=False)
    sectors = models.ManyToManyField(
        Sector, related_name='reach_responses', blank=True)

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


class PlanResponse(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(PlanQuestion, on_delete=models.CASCADE)
    media_plans = models.IntegerField(
        blank=True, null=True, verbose_name='Planes de nivel medio superior')
    superior_plans = models.IntegerField(
        blank=True, null=True, verbose_name='Planes de nivel superior')
    postgraduate_plans = models.IntegerField(
        blank=True, null=True, verbose_name='Planes de nivel posgrado')
    percentage = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True,
        verbose_name='Porcentaje general')

    def __str__(self):
        return f"Plan Response to '{self.question.text}'"

    class Meta:
        verbose_name = 'Respuesta a pregunta de Planes'
        verbose_name_plural = 'Respuestas a preguntas de Planes'


class BResponse(models.Model):
    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name='b_question_responses')
    question = models.ForeignKey(
        BQuestion, on_delete=models.CASCADE, related_name='responses')
    academic_instances_complying = models.IntegerField(blank=True, null=True)
    admin_instances_complying = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"Response to '{self.question.text}'"

    class Meta:
        verbose_name = 'Respuesta a pregunta B'
        verbose_name_plural = 'Respuestas a preguntas B'


    status_validation = models.ForeignKey(
        StatusControl, on_delete=models.CASCADE,
        related_name='a_responses')


class SpecialResponse(models.Model):
    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE,
        related_name='special_question_responses')
    question = models.ForeignKey(
        SpecialQuestion, on_delete=models.CASCADE,
        related_name='responses')
    total = models.IntegerField(blank=True, null=True)
    complying = models.IntegerField(blank=True, null=True)
    compliance_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = 'Respuesta a pregunta especial'
        verbose_name_plural = 'Respuestas a preguntas especiales'
