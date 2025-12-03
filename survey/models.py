from django.db import models

from indicator.models import PopulationQuestion
from pop.models import Sector


class PopulationResponse(models.Model):
    question = models.ForeignKey(
        PopulationQuestion, on_delete=models.CASCADE, related_name='responses')
    sectors = models.ManyToManyField(
        Sector, related_name='population_responses')

    def __str__(self):
        return f"Response to '{self.question.text}': {self.response_text}"
