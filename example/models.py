from django.db import models
from indicator.models import Axis, Component
from ies.models import User, Period, StatusControl, Institution


class Feature(models.Model):
    name = models.CharField(max_length=255)
    complement = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    reason_text = models.TextField(
        blank=True, null=True,
        verbose_name="Texto para justificar la calificación")
    order = models.IntegerField(default=0)
    is_other = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Característica a calificar"
        verbose_name_plural = "Características a calificar"


class FeatureOption(models.Model):
    feature = models.ForeignKey(
        Feature, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=255)
    value = models.IntegerField()

    def __str__(self):
        return f"{self.feature.name} - {self.name}"

    class Meta:
        ordering = ['feature__order', 'value']
        verbose_name = "Opción de característica"
        verbose_name_plural = "Opciones de características"


class GoodPracticePackage(models.Model):
    institution = models.ForeignKey(
        Institution, on_delete=models.CASCADE, related_name='packages')
    period = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='packages')
    status_sending = models.ForeignKey(
        StatusControl, on_delete=models.CASCADE, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Paquete de Buenas Prácticas - {self.institution.name} - {self.period.year}"

    class Meta:
        verbose_name = "Envío de Buenas Prácticas"
        verbose_name_plural = "Envío de Buenas Prácticas"


class GoodPractice(models.Model):
    package = models.ForeignKey(
        GoodPracticePackage, on_delete=models.CASCADE,
        related_name='good_practices')
    axis = models.ForeignKey(
        Axis, blank=True, null=True,
        on_delete=models.CASCADE, related_name='good_practices')
    component = models.ForeignKey(
        Component, blank=True, null=True,
        on_delete=models.CASCADE, related_name='good_practices')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    results = models.TextField(blank=True, null=True)
    final_value = models.IntegerField(blank=True, null=True)
    status_register = models.ForeignKey(
        StatusControl, on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        is_create = self._state.adding
        print("is_create:", is_create)
        super().save(*args, **kwargs)
        if is_create:
            all_features = Feature.objects.all()
            for feature in all_features:
                FeatureGoodPractice.objects.create(
                    good_practice=self,
                    feature=feature,
                )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Buena Práctica"
        verbose_name_plural = "Buenas Prácticas"


class FeatureGoodPractice(models.Model):
    good_practice = models.ForeignKey(
        GoodPractice, on_delete=models.CASCADE, related_name='feature_values')
    feature = models.ForeignKey(
        Feature, on_delete=models.CASCADE, related_name='good_practice_values')
    has_attribute = models.BooleanField(default=False)
    final_option = models.ForeignKey(
        FeatureOption, on_delete=models.CASCADE, blank=True, null=True)
    # status_validation = models.ForeignKey(
    #     StatusControl, on_delete=models.CASCADE, blank=True, null=True)
    justification = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    reviewers = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f"{self.good_practice.name} - {self.feature.name}"

    class Meta:
        verbose_name = "Valor de Característica de Buena Práctica"
        verbose_name_plural = "Valores de Características de Buenas Prácticas"


class Evidence(models.Model):
    good_practice = models.ForeignKey(
        GoodPractice, on_delete=models.CASCADE, blank=True, null=True,
        related_name='evidences')
    feature_good_practice = models.ForeignKey(
        FeatureGoodPractice, on_delete=models.CASCADE, blank=True, null=True,
        related_name='evidences')
    file = models.FileField(upload_to='evidences/')

    def __str__(self):
        return (f"Evidencia para "
                f"{(self.feature_good_practice or self.good_practice)}")

    class Meta:
        verbose_name = "Evidencia"
        verbose_name_plural = "Evidencias"
