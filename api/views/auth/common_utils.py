from django.conf import settings
from ies.models import InvitationToken, PasswordRecoveryToken


def get_destination_url(
        token: InvitationToken | PasswordRecoveryToken,
        param_url: str
):
    base = getattr(settings, 'FRONTEND_SITE_URL', '') or ''
    return f"{base}/{param_url}?token={token.key}"
