import logging

from django.core.mail import get_connection, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from .models import EmailProfile, TemplateBase, EmailRecord

logger = logging.getLogger(__name__)


def get_default_profile():
    """Return the default active EmailProfile, or any active one."""
    return (
        EmailProfile.objects.filter(
            is_default=True, is_active=True
        ).first()
        or EmailProfile.objects.filter(is_active=True).first()
    )


def build_connection(profile: EmailProfile):
    """Build a Django SMTP connection from an EmailProfile."""
    return get_connection(
        backend='django.core.mail.backends.smtp.EmailBackend',
        host=profile.get_host(),
        port=profile.port,
        username=profile.username,
        password=profile.get_password(),
        use_tls=profile.use_tls,
        use_ssl=profile.use_ssl,
    )


def _resolve_from_header(
    profile: EmailProfile,
    template: TemplateBase = None,
) -> str:
    """Build the From header, giving priority to the template's from_name."""
    from_email = profile.get_from_email()
    from_name = (
        (template.from_name if template else None)
        or profile.from_name
    )
    if from_name:
        return f"{from_name} <{from_email}>"
    return from_email


def send_template_email(
    template: TemplateBase,
    recipient_email: str,
    context: dict,
    user=None,
    profile: EmailProfile = None,
) -> EmailRecord:
    """
    Render a Django template and send it as an HTML email.
    Creates and returns an EmailRecord with the result.

    Args:
        template: TemplateBase instance (name = template path)
        recipient_email: destination address
        context: dict passed to render_to_string
        user: optional User that triggered the send
        profile: optional EmailProfile override
    """
    resolved_profile = (
        profile or template.profile or get_default_profile()
    )

    record = EmailRecord.objects.create(
        template_base=template,
        profile=resolved_profile,
        user=user,
        recipient_email=recipient_email,
        subject=template.subject,
        context_data=context,
        send_email=True,
    )

    if not resolved_profile:
        record.status = 'failed'
        record.errors = {
            'error': 'No email profile available'
        }
        record.save()
        return record

    try:
        html_body = render_to_string(template.name, context)
        from_header = _resolve_from_header(
            resolved_profile, template
        )
        connection = build_connection(resolved_profile)

        msg = EmailMultiAlternatives(
            subject=template.subject,
            body=html_body,
            from_email=from_header,
            to=[recipient_email],
            connection=connection,
        )
        msg.attach_alternative(html_body, 'text/html')
        msg.send()

        record.status = 'sent'
        record.sent_at = timezone.now()
        record.save()

    except Exception as exc:
        logger.exception(
            "Error sending template email to %s (template: %s)",
            recipient_email,
            template.name,
        )
        record.status = 'failed'
        record.errors = {'error': str(exc)}
        record.save()

    return record


def send_named_template_email(
    template_name: str,
    recipient_email: str,
    context: dict,
    user=None,
    profile: EmailProfile = None,
):
    """
    Look up a TemplateBase by name and send an HTML email.
    Logs a warning and returns None if the template is not found.
    Returns an EmailRecord (or None) with the result.

    Args:
        template_name: path relative to templates/ dir
            (e.g. 'email/password_recovery.html')
        recipient_email: destination address
        context: dict passed to render_to_string
        user: optional User that triggered the send
        profile: optional EmailProfile override
    """
    template = TemplateBase.objects.filter(
        name=template_name
    ).first()
    if not template:
        logger.warning(
            "TemplateBase '%s' not found. Email not sent.",
            template_name,
        )
        return None
    return send_template_email(
        template=template,
        recipient_email=recipient_email,
        context=context,
        user=user,
        profile=profile,
    )


def send_simple_email(
    recipient_email: str,
    subject: str,
    html_body: str,
    profile: EmailProfile = None,
    user=None,
) -> EmailRecord:
    """
    Send a one-off HTML email without a TemplateBase.
    Useful for quick notifications where no template exists.

    Args:
        recipient_email: destination address
        subject: email subject
        html_body: rendered HTML content
        profile: optional EmailProfile override
        user: optional User that triggered the send
    """
    resolved_profile = profile or get_default_profile()

    record = EmailRecord.objects.create(
        profile=resolved_profile,
        user=user,
        recipient_email=recipient_email,
        subject=subject,
        send_email=True,
    )

    if not resolved_profile:
        record.status = 'failed'
        record.errors = {
            'error': 'No email profile available'
        }
        record.save()
        return record

    try:
        from_header = _resolve_from_header(resolved_profile)
        connection = build_connection(resolved_profile)

        msg = EmailMultiAlternatives(
            subject=subject,
            body=html_body,
            from_email=from_header,
            to=[recipient_email],
            connection=connection,
        )
        msg.attach_alternative(html_body, 'text/html')
        msg.send()

        record.status = 'sent'
        record.sent_at = timezone.now()
        record.save()

    except Exception as exc:
        logger.exception(
            "Error sending simple email to %s",
            recipient_email,
        )
        record.status = 'failed'
        record.errors = {'error': str(exc)}
        record.save()

    return record