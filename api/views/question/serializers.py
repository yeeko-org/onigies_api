from rest_framework import serializers

from question.models import AOption


class AOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AOption
        fields = '__all__'
