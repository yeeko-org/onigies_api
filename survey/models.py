from django.db import models

from indicator.models import Axis, Component, Sector
from ies.models import Institution, Period


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
    media_plans = models.IntegerField(
        verbose_name='Planes a nivel medio superior')
    superior_plans = models.IntegerField(
        verbose_name='Planes a nivel superior')
    postgraduate_plans = models.IntegerField(
        verbose_name='Planes a nivel posgrado')

    def __str__(self):
        return f"Survey for {self.institution.name} during {self.period.name}"

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
