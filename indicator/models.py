from django.db import models


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

    def __str__(self):
        return f"{self.name} ({self.component.name})"

    class Meta:
        verbose_name = "Observable"
        verbose_name_plural = "Observables"


class Sector(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    needs_name = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    is_main = models.BooleanField(
        default=True, verbose_name="Es sector principal")

    def __unicode__(self):
        return self.name
