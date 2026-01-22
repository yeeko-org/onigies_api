from rest_framework import serializers

from example.models import (
    Feature, GoodPractice, FeatureOption, FeatureGoodPractice,
    GoodPracticePackage, Evidence)


class EvidenceSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="file.name")
    url = serializers.ReadOnlyField(source="file.url")

    class Meta:
        model = Evidence
        fields = ['id', 'file', 'name', 'url']


class FeatureOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureOption
        fields = '__all__'


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'


class FeatureFullSerializer(FeatureSerializer):
    feature_options = FeatureOptionSerializer(
        many=True, read_only=True, source='options')


class FeatureGoodPracticeSerializer(serializers.ModelSerializer):
    evidences = EvidenceSerializer(many=True, read_only=True)

    class Meta:
        model = FeatureGoodPractice
        fields = '__all__'


class GoodPracticeSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodPractice
        fields = '__all__'


class GoodPracticeFullSerializer(GoodPracticeSerializer):
    feature_values = FeatureGoodPracticeSerializer(many=True, read_only=True)
    evidences = EvidenceSerializer(many=True, read_only=True)


class GoodPracticePackageSerializer(serializers.ModelSerializer):
    good_practices = GoodPracticeFullSerializer(many=True, read_only=True)

    class Meta:
        model = GoodPracticePackage
        fields = '__all__'

