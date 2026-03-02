from rest_framework import serializers
from survey.models import Survey, PopulationQuantity


class PopulationQuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PopulationQuantity
        fields = '__all__'


class SurveySerializer(serializers.ModelSerializer):
    population_quantities = PopulationQuantitySerializer(
        many=True, read_only=True)
    class Meta:
        model = Survey
        fields = '__all__'
