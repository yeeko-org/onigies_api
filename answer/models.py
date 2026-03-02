from django.db import models

from indicator.models import Observable, Sector
from ies.models import User, StatusControl
from question.models import (
    QuestionType, ReachQuestion, AQuestion, AOption, PlanQuestion,
    BQuestion, SpecialQuestion)
from survey.models import Survey, Comment


class ObservableResponse(models.Model):

    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name='observable_responses')
    observable = models.ForeignKey(
        Observable, on_delete=models.CASCADE, related_name='responses')
    status_register = models.ForeignKey(
        StatusControl, on_delete=models.CASCADE)
    value = models.BooleanField(
        blank=True, null=True, verbose_name='Respuesta a pregunta inicial')

    def __str__(self):
        return f"Response to '{self.observable}' ({self.survey})"

    class Meta:
        verbose_name = 'Respuesta observable'
        verbose_name_plural = 'Respuestas observables'


class ObservableComment(Comment):
    observable_response = models.ForeignKey(
        ObservableResponse, on_delete=models.CASCADE,
        related_name='comments')

    class Meta:
        verbose_name = 'Comentario de respuesta observable'
        verbose_name_plural = 'Comentarios de respuestas observables'


class GroupResponse(models.Model):
    observable_response = models.ForeignKey(
        ObservableResponse, on_delete=models.CASCADE,
        related_name='statuses')
    question_type = models.ForeignKey(
        QuestionType, on_delete=models.CASCADE,
        related_name='group_responses')
    status_register = models.ForeignKey(
        StatusControl, on_delete=models.CASCADE)
    value = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return "Group Response"

    class Meta:
        verbose_name = 'Grupo de Respuestas (por tipo)'
        verbose_name_plural = 'Grupos de Respuestas (por tipo)'


class GroupComment(Comment):
    group_response = models.ForeignKey(
        GroupResponse, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        verbose_name = 'Comentario de encuesta'
        verbose_name_plural = 'Comentarios de encuestas'


def set_upload_attachment_path(instance, filename):
    from utils.files import join_path

    elems = ['attachments']
    group_response: GroupResponse = instance.group_response
    observable_response = group_response.observable_response
    survey = observable_response.survey
    elems.append(survey.institution.acronym)
    year = str(survey.period_id)
    observable = observable_response.observable
    axis = observable.component.axis.short_name
    elems.append(f'{year}_{axis}')
    elems.append(f'observable_{observable.number}')
    return join_path(elems, filename)


class GroupAttachment(models.Model):
    group_response = models.ForeignKey(
        GroupResponse, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(
        upload_to=set_upload_attachment_path, verbose_name="Archivo")

    def __str__(self):
        return "%s - %s" % (self.group_response, self.file.name)

    class Meta:
        verbose_name = "Comprobable de grupo de respuestas"
        verbose_name_plural = "Comprobables de grupos de respuestas"


class AResponse(models.Model):
    group_response = models.ForeignKey(
        GroupResponse, on_delete=models.CASCADE,
        related_name='a_responses')
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


class ReachResponse(models.Model):
    group_response = models.ForeignKey(
        GroupResponse, on_delete=models.CASCADE,
        related_name='reach_responses')
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


class PlanResponse(models.Model):
    group_response = models.ForeignKey(
        GroupResponse, on_delete=models.CASCADE,
        related_name='plan_responses')
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
    group_response = models.ForeignKey(
        GroupResponse, on_delete=models.CASCADE,
        related_name='b_responses')
    question = models.ForeignKey(
        BQuestion, on_delete=models.CASCADE, related_name='responses')
    academic_instances_complying = models.IntegerField(blank=True, null=True)
    admin_instances_complying = models.IntegerField(blank=True, null=True)
    percentage = models.DecimalField(
        max_digits=5, decimal_places=2,
        blank=True, null=True, verbose_name='Porcentaje general')

    def __str__(self):
        return f"Response to '{self.question.text}'"

    class Meta:
        verbose_name = 'Respuesta a pregunta B'
        verbose_name_plural = 'Respuestas a preguntas B'


class SpecialResponse(models.Model):
    group_response = models.ForeignKey(
        GroupResponse, on_delete=models.CASCADE,
        related_name='special_responses')
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
