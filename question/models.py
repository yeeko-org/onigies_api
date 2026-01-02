from django.db import models

from indicator.models import Observable, Sector


# QUESTION_GROUPS = [
#     ('a_questions', 'Institucionalización', 'a_weight', 'AQuestion'),
#     ('b_questions', 'Instancias', 'b_weight', 'BQuestion'),
#     ('population', 'Sectores', 'pop_weight', 'PopulationQuestion'),
#     ('plans', 'Planes de estudio', 'plan_weight', 'PlanQuestion'),
#     ('special', 'Pregunta especial', 'special_weight', 'SpecialQuestion')
# ]

class QuestionGroup(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    weight_name = models.CharField(max_length=40)
    public_name = models.CharField(max_length=150)
    model_name = models.CharField(max_length=50)
    default_weight = models.DecimalField(
        max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Grupo de preguntas"
        verbose_name_plural = "Grupos de preguntas"


class AQuestion(models.Model):

    text = models.TextField()
    observable = models.ForeignKey(Observable, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pregunta: {self.text} ({self.observable.name})"

    class Meta:
        verbose_name = "Pregunta de institucionalización"
        verbose_name_plural = "Preguntas de institucionalización"


class AOption(models.Model):
    text = models.CharField(max_length=255)
    value = models.IntegerField()

    def __str__(self):
        return f"Opción de respuesta: {self.text} (Valor: {self.value})"

    class Meta:
        verbose_name = "Opción de respuesta de institucionalización"
        verbose_name_plural = "Opciones de respuesta de institucionalización"


class PopulationQuestion(models.Model):

    text = models.TextField()
    observable = models.ForeignKey(Observable, on_delete=models.CASCADE)
    has_main_sectors = models.BooleanField(
        default=True, verbose_name="Tiene los sectores principales")
    others_sectors = models.ManyToManyField(Sector, blank=True)
    has_general_planning = models.BooleanField(
        default=False, verbose_name="Tiene la opción de planeación general")

    def __str__(self):
        return f"Pregunta población: {self.text} ({self.observable.name})"

    class Meta:
        verbose_name = "Pregunta de población"
        verbose_name_plural = "Preguntas de población"


class PlanQuestion(models.Model):
    observable = models.ForeignKey(Observable, on_delete=models.CASCADE)
    text = models.TextField()


class BQuestion(models.Model):

    observable = models.ForeignKey(Observable, on_delete=models.CASCADE)
    order = models.IntegerField(default=10)
    text = models.TextField()
    includes_academic = models.BooleanField(
        blank=True, null=True,
        verbose_name="Incluye entidades académicas")
    includes_admin = models.BooleanField(
        blank=True, null=True,
        verbose_name="Incluye dependencias administrativas")

    def __str__(self):
        return f"Pregunta cuerpo: {self.text} ({self.observable.name})"

    class Meta:
        verbose_name = "Pregunta de cuerpo"
        verbose_name_plural = "Preguntas de cuerpo"


class SpecialQuestion(models.Model):

    text = models.TextField()
    observable = models.ForeignKey(Observable, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pregunta especial: {self.text} ({self.observable.name})"

    class Meta:
        verbose_name = "Pregunta especial"
        verbose_name_plural = "Preguntas especiales"



