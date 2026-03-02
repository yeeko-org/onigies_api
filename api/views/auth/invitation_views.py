import logging

from django.conf import settings
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from api.mixins import MultiSerializerCreateRetrieveMix
from api.permissions import IsAdminOrReadOnly, IsReviewer
from api.views.auth.serializers import (
    InvitationTokenCreateSerializer,
    InvitationTokenDetailSerializer,
    InvitationTokenListSerializer,
    UserDataSerializer,
    UserRegistrationFromInvitationSerializer,
)
from ies.models import InvitationToken

logger = logging.getLogger(__name__)
_GENERIC_ALREADY_USED_MESSAGE = 'La invitación ya ha sido utilizada.'


def _send_invitation_email(token: InvitationToken):
    from api.views.auth.common_utils import get_destination_url
    from email_send.service import send_named_template_email

    context = {
        'destination_url': get_destination_url(token, 'register'),
    }
    if token.institution:
        context['institution'] = token.institution
        template_name = 'email/invitation_institution.html'
    else:
        template_name = 'email/invitation_generic.html'
    send_named_template_email(
        template_name=template_name,
        recipient_email=token.email,
        context=context,
    )


class InvitationTokenViewSet(MultiSerializerCreateRetrieveMix):
    """
    list     GET    /api/invitation/                (reviewer)
    create   POST   /api/invitation/                (reviewer)
    retrieve GET    /api/invitation/<key>/          (anyone)
    destroy  DELETE /api/invitation/<key>/          (admin)
    register POST   /api/invitation/<key>/register/ (anyone)
    """

    queryset = InvitationToken.objects.select_related(
        'institution', 'user'
    ).order_by('-created_at')
    serializer_class = InvitationTokenListSerializer
    action_serializers = {
        'list': InvitationTokenListSerializer,
        'create': InvitationTokenCreateSerializer,
        'retrieve': InvitationTokenDetailSerializer,
        'register': UserRegistrationFromInvitationSerializer,
    }

    def get_permissions(self):
        if self.action in ('retrieve', 'register'):
            return [permissions.AllowAny()]
        if self.action == 'destroy':
            return [IsAdminOrReadOnly()]
        return [IsReviewer()]

    def get_queryset(self):
        qs = super().get_queryset()
        institution = self.request.query_params.get('institution')
        no_institution = self.request.query_params.get(
            'no_institution', ''
        )
        if institution:
            qs = qs.filter(institution_id=institution)
        elif no_institution.lower() in ('true', '1'):
            qs = qs.filter(institution__isnull=True)
        return qs

    def perform_create(self, serializer):
        token = serializer.save()
        try:
            _send_invitation_email(token)
        except Exception:
            logger.exception(
                "Error al enviar el correo de invitación para token %s",
                token.key,
            )

    def retrieve(self, request, *args, **kwargs):
        token = self.get_object()
        if token.used_at:
            return Response(
                {'detail': _GENERIC_ALREADY_USED_MESSAGE},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not token.viewed_at:
            token.viewed_at = timezone.now()
            token.save(update_fields=['viewed_at'])
        return Response(self.get_serializer(token).data)

    @action(
        detail=True,
        methods=['post'],
        url_path='register',
        url_name='register',
    )
    def register(self, request, pk=None):
        try:
            token = InvitationToken.objects.select_related(
                'institution'
            ).get(pk=pk)
        except InvitationToken.DoesNotExist:
            raise NotFound('Token de invitación no encontrado.')

        if token.used_at:
            return Response(
                {'detail': _GENERIC_ALREADY_USED_MESSAGE},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        from ies.models import User
        from rest_framework.authtoken.models import (
            Token as AuthToken)

        user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            username=data['email'],
            password_changed=True,
        )
        if token.institution:
            user.institution = token.institution
        else:
            user.reviewer = token.reviewer
            user.is_staff = token.is_staff
            user.is_superuser = token.is_superuser
        user.set_password(data['password'])
        user.save()

        AuthToken.objects.get_or_create(user=user)

        token.user = user
        token.used_at = timezone.now()
        token.save(update_fields=['user', 'used_at'])

        return Response(
            UserDataSerializer(user, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )