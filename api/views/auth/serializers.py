from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from ies.models import User, InvitationToken
from api.views.ies.serializers import (
    InstitutionFullSerializer, InstitutionSimpleSerializer)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(
        required=True, style={'input_type': 'password'})
    key = serializers.CharField(required=False)


class UserDataSerializer(serializers.ModelSerializer):
    fullname = serializers.ReadOnlyField(source="full_name")
    token = serializers.ReadOnlyField(source="auth_token.key")
    institution = InstitutionFullSerializer(read_only=True)
    is_ies = serializers.SerializerMethodField()
    is_full_editor = serializers.ReadOnlyField(source="full_editor")

    def get_is_ies(self, obj):
        return obj.institution is not None

    class Meta(object):
        model = User
        fields = [
            "id", 'email', 'username', "first_name", "last_name",
            "token", "fullname", "full_editor", "is_staff",
            "is_superuser", "institution", "is_ies", "is_full_editor"]


class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.get_full_name()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "is_staff",
            "is_superuser",
            "first_name",
            "last_name",
            "full_editor",
            "full_name",
        ]


class UserSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    password = serializers.CharField(
        min_length=8,
        style={ 'input_type': 'password' })
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
        required=False,
        validators=[UniqueValidator(queryset=User.objects.all())])
    checkCondiction = serializers.BooleanField(
        required=False)
    key = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "last_login",
            "is_superuser",
            "username",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "is_staff",
            "is_active",
            "date_joined"
        ]
        # read_only_fields = [
        #     "last_login",
        #     "is_superuser",
        #     "username",
        #     "full_name",
        #     "is_staff",
        #     "is_active",
        #     "date_joined"
        # ]


class UserRegistrationSerializer(UserDataSerializer):

    class Meta:
        model = User
        fields = UserDataSerializer.Meta.fields + ["password"]
        # read_only_fields = UserDataSerializer.Meta.read_only_fields



class InvitationTokenSerializer(serializers.ModelSerializer):
    institution_full = InstitutionSimpleSerializer(
        read_only=True, source='institution')

    class Meta:
        model = InvitationToken
        fields = ["email", "institution", "institution_full"]
