from django.db import models


class Sector(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    needs_name = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    is_generic = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class Unity(models.Model):
    # academic_entity, admin_entity, media plans, superior plans,
    # postgraduate plans
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Unidad de medida"
        verbose_name_plural = "Unidades de medida"




