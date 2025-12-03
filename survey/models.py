from django.db import models

from indicator.models import PopulationQuestion, Observable
from ies.models import Institution
from space_time.models import Period
from pop.models import Sector


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
    ('partial', 'Parcialmente'),
)

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
    sectors = models.ManyToManyField(
        Sector, related_name='population_responses')
    not_focalized = models.BooleanField(
        verbose_name='No focalizado en sectores específicos',
        default=False)

    def __str__(self):
        return f"Response to '{self.question.text}'"

    class Meta:
        verbose_name = 'Respuesta de población'
        verbose_name_plural = 'Respuestas de población'


class PopulationQuantity(models.Model):
    response = models.ForeignKey(
        PopulationResponse, on_delete=models.CASCADE, related_name='quantities')
    sector = models.ForeignKey(
        Sector, on_delete=models.CASCADE, related_name='population_quantities')
    number_men = models.PositiveIntegerField(
        verbose_name='Número de hombres')
    number_women = models.PositiveIntegerField(
        verbose_name='Número de mujeres')

    def __str__(self):
        return f"{self.sector.name}: {self.number_men} hombres, {self.number_women} mujeres"

    class Meta:
        verbose_name = 'Cantidad de población por sector'
        verbose_name_plural = 'Cantidades de población por sector'
