from rest_framework import serializers
from ies.models import Period, Institution
from survey.models import Survey
from example.models import GoodPracticePackage


class PeriodSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = '__all__'


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


class GoodPracticePackageSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodPracticePackage
        fields = '__all__'


class InstitutionSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'


class InstitutionFullSerializer(serializers.ModelSerializer):
    surveys = SurveySerializer(many=True, read_only=True)
    packages = GoodPracticePackageSimpleSerializer(
        many=True, read_only=True)

    class Meta:
        model = Institution
        fields = '__all__'
