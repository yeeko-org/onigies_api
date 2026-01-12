from rest_framework import serializers
from ies.models import Period, Institution

class PeriodSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = '__all__'


class InstitutionSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'
