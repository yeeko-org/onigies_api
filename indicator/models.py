from django.db import models

from ies.models import StatusControl, User


class GeneralGroup(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    public_name = models.CharField(max_length=150)
    fields = models.JSONField(default=list, blank=True)
    is_population = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Grupo de preguntas (Generales)"
        verbose_name_plural = "Grupos de preguntas (Generales)"


class Axis(models.Model):
    order = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, unique=True)
    short_name = models.CharField(max_length=100, blank=True, null=True)
    slug = models.CharField(max_length=55, blank=True, null=True)
    # logo = models.ImageField(blank=True, null=True, upload_to='axis_logos')
    icon = models.CharField(max_length=55, blank=True, null=True)
    color = models.CharField(max_length=55)
    hex_color = models.CharField(max_length=7, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name = "Materia (Axis)"
        verbose_name_plural = "Materias (Axes)"


class Component(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    axis = models.ForeignKey(Axis, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.axis.name})"

    class Meta:
        verbose_name = "Componente"
        verbose_name_plural = "Componentes"


class Observable(models.Model):

    component = models.ForeignKey(
        Component, on_delete=models.CASCADE, related_name='observables')

    number = models.DecimalField(max_digits=4, decimal_places=2)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    init_question = models.TextField(blank=True, null=True)
    a_main_question = models.TextField(
        blank=True, null=True,
        verbose_name="Pregunta institucionalización")
    a_main_subtitle = models.TextField(
        blank=True, null=True,
        verbose_name="Subtítulo institucionalización")

    a_weight = models.DecimalField(
        max_digits=5, decimal_places=2,
        blank=True, null=True,
        verbose_name="Ponderación institucionalización")
    b_weight = models.DecimalField(
        max_digits=5, decimal_places=2,
        blank=True, null=True,
        verbose_name="Ponderación cumplimiento")
    reach_weight = models.DecimalField(
        max_digits=5, decimal_places=2,
        blank=True, null=True,
        verbose_name="Ponderación alcance de población")
    plan_weight = models.DecimalField(
        max_digits=5, decimal_places=2,
        blank=True, null=True,
        verbose_name="Ponderación de planes")
    special_weight = models.DecimalField(
        max_digits=5, decimal_places=2,
        blank=True, null=True,
        verbose_name="Ponderación especial")
    pop_weight = models.DecimalField(
        max_digits=5, decimal_places=2,
        blank=True, null=True,
        verbose_name="Ponderación población")

    def get_default_weight(self, weight_field):
        from question.models import QuestionType
        weight_value = getattr(self, weight_field)
        if weight_value is not None:
            return weight_value
        try:
            question_type = QuestionType.objects.get(weight_name=weight_field)
            return question_type.default_weight
        except QuestionType.DoesNotExist:
            return None

    @property
    def final_a_weight(self):
        return self.get_default_weight('a_weight')

    def final_b_weight(self):
        return self.get_default_weight('b_weight')

    def final_reach_weight(self):
        return self.get_default_weight('reach_weight')

    def final_plan_weight(self):
        return self.get_default_weight('plan_weight')

    def final_special_weight(self):
        return self.get_default_weight('special_weight')

    def final_pop_weight(self):
        return self.get_default_weight('pop_weight')

    def __str__(self):
        return f"{self.name} ({self.component.name})"

    class Meta:
        verbose_name = "Observable (Pregunta inicial)"
        verbose_name_plural = "Observables (Preguntas iniciales)"


class Sector(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    needs_name = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    is_main = models.BooleanField(
        default=True, verbose_name="Es sector principal")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name = "Sector"
        verbose_name_plural = "Sectores"
