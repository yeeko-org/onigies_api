from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.views.common_serializers import InvitationTokenSimpleSerializer
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
    institution = InstitutionSimpleSerializer(read_only=True)
    institution_details = InstitutionFullSerializer(
        read_only=True, source="institution")
    is_ies = serializers.SerializerMethodField()
    is_reviewer = serializers.ReadOnlyField(source="reviewer")

    def get_is_ies(self, obj):
        return obj.institution is not None

    class Meta(object):
        model = User
        fields = [
            "id", 'email', 'username', "first_name", "last_name",
            "token", "fullname", "reviewer", "is_staff",
            "is_superuser", "institution", "institution_details",
            "is_ies", "is_reviewer"]


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
            "reviewer",
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


class PasswordRecoveryRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        return value.strip().lower()


class InvitationTokenCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitationToken
        fields = [
            'email', 'institution',
            'reviewer', 'is_staff', 'is_superuser',
        ]

    def validate(self, data):
        institution = data.get('institution')
        email = data.get('email')
        if not institution and not email:
            raise serializers.ValidationError({
                'email': (
                    'El email es obligatorio cuando no se '
                    'asocia una institución.'
                )
            })
        return data


class InvitationTokenListSerializer(InvitationTokenSimpleSerializer):
    institution_full = InstitutionSimpleSerializer(
        read_only=True, source='institution')

    class Meta:
        model = InvitationToken
        fields = InvitationTokenSimpleSerializer.Meta.fields + ['institution_full']


class InvitationTokenDetailSerializer(InvitationTokenListSerializer):
    class Meta(InvitationTokenListSerializer.Meta):
        pass


class PasswordRecoveryConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(
        required=True,
        min_length=8,
        style={'input_type': 'password'},
    )
    password_confirm = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
    )

    def validate(self, data):
        if data['password'] != data.get('password_confirm'):
            raise serializers.ValidationError({
                'password_confirm': (
                    'Las contraseñas no coinciden.'
                ),
            })
        return data


class UserRegistrationFromInvitationSerializer(
    PasswordRecoveryConfirmSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                'Ya existe un usuario registrado con este correo.'
            )
        return value.lower()
