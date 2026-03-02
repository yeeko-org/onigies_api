from django.db import models

from indicator.models import Axis, Component, Sector, GeneralGroup
from ies.models import Institution, Period, StatusControl, Instance, User


class Comment(models.Model):
    text = models.TextField(verbose_name='Texto del comentario')
    status_register = models.ForeignKey(
        StatusControl, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Comment"

    class Meta:
        abstract = True


class Survey(models.Model):

    institution = models.ForeignKey(
        Institution, on_delete=models.CASCADE, related_name='surveys')
    period = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='surveys')
    is_centralized = models.BooleanField(
        blank=True, null=True,
        help_text="Gobierno centralizado")
    academic_instances = models.IntegerField(
        verbose_name='Instancias académicas', blank=True, null=True)
    admin_instances = models.IntegerField(
        verbose_name='Instancias administrativas', blank=True, null=True)
    instances = models.ManyToManyField(
        Instance, related_name='surveys',
        verbose_name='Instancias', blank=True)
    sectors = models.ManyToManyField(
        Sector, related_name='surveys',
        verbose_name='Sectores atendidos', blank=True)
    media_plans = models.IntegerField(
        verbose_name='Planes a nivel medio superior', blank=True, null=True)
    superior_plans = models.IntegerField(
        verbose_name='Planes a nivel superior', blank=True, null=True)
    postgraduate_plans = models.IntegerField(
        verbose_name='Planes a nivel posgrado', blank=True, null=True)

    def __str__(self):
        return f"Survey: {self.institution.name} - {self.period}"

    class Meta:
        unique_together = ('institution', 'period')
        verbose_name = 'Conjunto de respuestas IES-Año'
        verbose_name_plural = 'Conjuntos de respuestas IES-Año'


class AxisValue(models.Model):
    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name='axis_values')
    axis = models.ForeignKey(
        Axis, on_delete=models.CASCADE, related_name='axis_values')
    value = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)
    status_register = models.ForeignKey(
        StatusControl, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.axis.name}: {self.value}"

    class Meta:
        verbose_name = 'Valor del eje'
        verbose_name_plural = 'Valores de los ejes'


class ComponentValue(models.Model):
    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name='component_values')
    component = models.ForeignKey(
        Component, on_delete=models.CASCADE, related_name='component_values')
    value = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.component.name}: {self.value}"

    class Meta:
        verbose_name = 'Valor del componente'
        verbose_name_plural = 'Valores de los componentes'


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


class GeneralGroupResponse(models.Model):
    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE,
        related_name='general_group_responses')
    general_group = models.ForeignKey(
        GeneralGroup, on_delete=models.CASCADE,
        related_name='general_group_responses')
    status_register = models.ForeignKey(
        StatusControl, on_delete=models.CASCADE)

    def __str__(self):
        return (f"Respuesta del grupo general "
                f"'{self.general_group}' ({self.survey})")

    class Meta:
        verbose_name = 'Grupo de Respuestas General'
        verbose_name_plural = 'Grupos de Respuestas Generales'


class GeneralGroupComment(Comment):
    general_group_response = models.ForeignKey(
        GeneralGroupResponse, on_delete=models.CASCADE,
        related_name='comments')

    class Meta:
        verbose_name = 'Comentario a grupo de respuestas (General)'
        verbose_name_plural = 'Comentarios a grupos de respuestas (General)'


def set_upload_general_attachment_path(instance, filename):
    from utils.files import join_path

    elems = ['attachments']
    gg_response: GeneralGroupResponse = instance.general_group_response

    survey = gg_response.survey
    elems.append(survey.institution.acronym)
    year = str(survey.period_id)
    elems.append(f'{year}_general')
    general_group = gg_response.general_group.name
    elems.append(f'group_{general_group}')
    return join_path(elems, filename)


class GeneralGroupAttachment(models.Model):
    general_group_response = models.ForeignKey(
        GeneralGroupResponse, on_delete=models.CASCADE,
        related_name='attachments')
    file = models.FileField(
        upload_to=set_upload_general_attachment_path, verbose_name="Archivo")

    def __str__(self):
        return "%s - %s" % (self.general_group_response, self.file.name)

    class Meta:
        verbose_name = "Comprobable de grupo general de respuestas"
        verbose_name_plural = "Comprobables de grupos generales de respuestas"
