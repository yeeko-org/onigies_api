from django.contrib.admin import register, ModelAdmin
from .models import Survey

# class Survey(models.Model):
#
#     institution = models.ForeignKey(
#         Institution, on_delete=models.CASCADE, related_name='surveys')
#     period = models.ForeignKey(
#         Period, on_delete=models.CASCADE, related_name='surveys')
#     is_centralized = models.BooleanField(
#         blank=True, null=True,
#         help_text="Gobierno centralizado")
#     academic_instances = models.IntegerField(
#         verbose_name='Instancias académicas', blank=True, null=True)
#     admin_instances = models.IntegerField(
#         verbose_name='Instancias administrativas', blank=True, null=True)
#     instances = models.ManyToManyField(
#         Instance, related_name='surveys',
#         verbose_name='Instancias', blank=True)
#     sectors = models.ManyToManyField(
#         Sector, related_name='surveys',
#         verbose_name='Sectores atendidos', blank=True)
#     media_plans = models.IntegerField(
#         verbose_name='Planes a nivel medio superior', blank=True, null=True)
#     superior_plans = models.IntegerField(
#         verbose_name='Planes a nivel superior', blank=True, null=True)
#     postgraduate_plans = models.IntegerField(
#         verbose_name='Planes a nivel posgrado', blank=True, null=True)
#
#     def __str__(self):
#         return f"Survey: {self.institution.name} - {self.period}"
#
#     class Meta:
#         unique_together = ('institution', 'period')
#         verbose_name = 'Conjunto de respuestas IES-Año'
#         verbose_name_plural = 'Conjuntos de respuestas IES-Año'

@register(Survey)
class SurveyAdmin(ModelAdmin):
    list_display = ('institution', 'period', 'is_centralized')
    list_filter = ('period', 'is_centralized')
    search_fields = ('institution__name', 'period__year')
    filter_horizontal = ('instances', 'sectors')