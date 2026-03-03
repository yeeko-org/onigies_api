from rest_framework import serializers

from ies.models import InvitationToken


class InvitationTokenBaseSerializer(serializers.ModelSerializer):
    destination_url = serializers.SerializerMethodField()

    def get_destination_url(self, obj):
        from api.views.auth.common_utils import get_destination_url
        return get_destination_url(obj, 'register')

    class Meta:
        model = InvitationToken
        fields = [
            'key', 'email', 'institution',
            'created_at', 'viewed_at', 'used_at',
            'reviewer', 'is_staff', 'is_superuser',
            'destination_url', 'email_sent',
        ]
