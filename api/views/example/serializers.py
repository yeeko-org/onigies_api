from rest_framework import serializers

from example.models import (
    Feature, GoodPractice, FeatureOption, FeatureGoodPractice,
    GoodPracticePackage)


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



class GoodPracticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodPractice
        fields = '__all__'


class FeatureGoodPracticeSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeatureGoodPractice
        fields = '__all__'


class GoodPracticePackageSerializer(serializers.ModelSerializer):
    good_practices = GoodPracticeSerializer(many=True, read_only=True)

    class Meta:
        model = GoodPracticePackage
        fields = '__all__'

