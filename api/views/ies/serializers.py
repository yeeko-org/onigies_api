from rest_framework import serializers
from ies.models import Period, Institution
from survey.models import Survey, AxisValue
from example.models import GoodPracticePackage
from api.views.common_serializers import InvitationTokenSimpleSerializer


class PeriodSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = '__all__'


class AxisValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AxisValue
        fields = '__all__'


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


class SurveyFullSerializer(SurveySerializer):
    axis_values = AxisValueSerializer(many=True, read_only=True)


class GoodPracticePackageSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodPracticePackage
        fields = '__all__'


class InstitutionSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'


class InstitutionDetailSerializer(serializers.ModelSerializer):
    invitation_tokens = InvitationTokenSimpleSerializer(
        many=True, read_only=True)

    class Meta:
        model = Institution
        fields = '__all__'


class InstitutionSerializer(serializers.ModelSerializer):
    good_practice_packages_count = serializers.ReadOnlyField()
    good_practices_count = serializers.ReadOnlyField()

    class Meta:
        model = Institution
        fields = '__all__'


class InstitutionFullSerializer(serializers.ModelSerializer):
    surveys = SurveyFullSerializer(many=True, read_only=True)
    packages = GoodPracticePackageSimpleSerializer(
        many=True, read_only=True)

    class Meta:
        model = Institution
        fields = '__all__'
