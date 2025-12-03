from django.db import models


class Sector(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)
    is_generic = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


