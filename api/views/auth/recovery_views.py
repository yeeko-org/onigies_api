import logging

from django.conf import settings
from django.utils import timezone
from rest_framework import views, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

logger = logging.getLogger(__name__)

_INVALID_TOKEN_MSG = (
    'El token ha expirado o ya fue utilizado.'
)
_GENERIC_OK_MSG = (
    'Si el correo existe, recibirás un enlace '
    'de recuperación en breve.'
)


def _invalidate_previous_tokens(user):
    """Mark all open recovery tokens for user as used."""
    from ies.models import PasswordRecoveryToken
    PasswordRecoveryToken.objects.filter(
        user=user, used_at__isnull=True
    ).update(used_at=timezone.now())


def _get_token_or_404(key):
    from ies.models import PasswordRecoveryToken
    try:
        return PasswordRecoveryToken.objects.select_related(
            'user'
        ).get(key=key)
    except PasswordRecoveryToken.DoesNotExist:
        raise NotFound('Token inválido.')


class PasswordRecoveryRequestView(views.APIView):
    """
    POST /api/password-recovery/

    Request a password recovery email.
    Always returns HTTP 200 to avoid email enumeration.

    Body: { "email": "user@example.com" }
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        from .serializers import PasswordRecoveryRequestSerializer
        serializer = PasswordRecoveryRequestSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        self._process(serializer.validated_data['email'])
        return Response({'detail': _GENERIC_OK_MSG})

    def _process(self, email):
        from api.views.auth.common_utils import get_destination_url
        from email_send.service import send_named_template_email
        from ies.models import User, PasswordRecoveryToken
        user = User.objects.filter(
            email__iexact=email, is_active=True
        ).first()
        if not user:
            return
        _invalidate_previous_tokens(user)
        token = PasswordRecoveryToken.objects.create(user=user)
        try:
            destination_url = get_destination_url(token, 'recover-password')
            context = {
                'user': {
                    'full_name': user.get_full_name(),
                    'email': user.email,
                },
                'expiry_hours': token.EXPIRY_HOURS,
                'destination_url': destination_url,
            }
            send_named_template_email(
                template_name='email/password_recovery.html',
                recipient_email=email,
                context=context,
            )
        except Exception:
            logger.exception(
                "Unexpected error sending recovery email to %s",
                email,
            )


class PasswordRecoveryValidateView(views.APIView):
    """
    GET /api/password-recovery/{key}/

    Validate that a token is still usable.
    Returns basic user info to display in the frontend form.
    Does NOT consume the token.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, key):
        token = _get_token_or_404(key)
        if not token.is_valid():
            return Response(
                {'detail': _INVALID_TOKEN_MSG},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({
            'email': token.user.email,
            'full_name': token.user.get_full_name(),
            'valid': True,
        })


class PasswordRecoveryConfirmView(views.APIView):
    """
    POST /api/password-recovery/{key}/confirm/

    Set a new password using a valid recovery token.

    Body: {
        "password": "new_password",
        "password_confirm": "new_password"
    }
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, key):
        from .serializers import PasswordRecoveryConfirmSerializer
        from rest_framework.authtoken.models import Token as AuthToken
        from api.views.auth.serializers import UserDataSerializer

        token = _get_token_or_404(key)
        if not token.is_valid():
            return Response(
                {'detail': _INVALID_TOKEN_MSG},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = PasswordRecoveryConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = token.user
        user.set_password(serializer.validated_data['password'])
        user.password_changed = True
        user.save()
        token.mark_used()

        # Ensure auth token exists and return full user data
        # so the frontend can log in immediately (same as /login/).
        AuthToken.objects.get_or_create(user=user)
        out_serializer = UserDataSerializer(user, context={ 'request': request})
        return Response(out_serializer.data)
