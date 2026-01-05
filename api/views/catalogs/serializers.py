from rest_framework import serializers
from ies.models import StatusControl
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
