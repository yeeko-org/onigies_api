from rest_framework import serializers

from indicator.models import  Axis, Component, Observable, Sector



class ObservableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observable
        fields = '__all__'


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = '__all__'


class ComponentFullSerializer(serializers.ModelSerializer):
    observables = ObservableSerializer(many=True, read_only=True)
    # observables_count = serializers.SerializerMethodField()
    #
    # def get_observables_count(self, obj: Component):
    #     return obj.observables.count()

    class Meta:
        model = Component
        fields = '__all__'


class AxisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Axis
        fields = '__all__'


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = '__all__'






