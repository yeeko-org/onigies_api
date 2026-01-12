from rest_framework import serializers
from ies.models import StatusControl, Institution, Period
from ps_schema.models import Level, Collection, FilterGroup


class StatusControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusControl
        fields = "__all__"


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = "__all__"


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = "__all__"


class FilterGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterGroup
        fields = "__all__"


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = "__all__"


class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = "__all__"
