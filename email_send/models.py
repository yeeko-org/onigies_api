from django.db import models


PROVIDER_CHOICES = [
    ('gmail', 'Gmail'),
    ('outlook', 'Outlook / Microsoft 365'),
    ('custom', 'Personalizado'),
]

HOST_PRESETS = {
    'gmail': 'smtp.gmail.com',
    'outlook': 'smtp.office365.com',
}


class EmailProfile(models.Model):
    name = models.CharField(max_length=100, unique=True)
    provider = models.CharField(
        max_length=20,
        choices=PROVIDER_CHOICES,
        default='gmail',
    )
    host = models.CharField(
        max_length=200,
        blank=True,
        help_text="Vacío = usar preset del proveedor",
    )
    port = models.IntegerField(default=587)
    use_tls = models.BooleanField(default=True)
    use_ssl = models.BooleanField(default=False)
    username = models.EmailField()
    password_env_var = models.CharField(
        max_length=100,
        help_text=(
            "Nombre de la variable de entorno "
            "que contiene la contraseña/app token"
        ),
    )
    from_email = models.EmailField(
        blank=True,
        help_text="Vacío = usar username como remitente",
    )
    from_name = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(
        default=False,
        help_text="Perfil usado cuando el template no especifica uno",
    )

    def get_host(self):
        if self.host:
            return self.host
        return HOST_PRESETS.get(self.provider, '')

    def get_password(self):
        import os
        return os.getenv(self.password_env_var, '')

    def get_from_email(self):
        return self.from_email or self.username

    def get_from_header(self):
        if self.from_name:
            return f"{self.from_name} <{self.get_from_email()}>"
        return self.get_from_email()

    def __str__(self):
        return f"{self.name} ({self.get_provider_display()})"

    class Meta:
        verbose_name = "Perfil de correo"
        verbose_name_plural = "Perfiles de correo"


class TemplateBase(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text=(
            "Ruta del template relativa a templates/ "
            "(ej: email/invitation.html)"
        ),
    )
    subject = models.CharField(max_length=200)
    from_name = models.CharField(
        max_length=200,
        blank=True,
        help_text=(
            "Sobrescribe el from_name del perfil para este template"
        ),
    )
    description = models.TextField(blank=True, null=True)
    profile = models.ForeignKey(
        EmailProfile,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='templates',
        help_text="Vacío = usar el perfil default activo",
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Template de correo"
        verbose_name_plural = "Templates de correo"


EMAIL_STATUS_CHOICES = [
    ('pending', 'Pendiente'),
    ('sent', 'Enviado'),
    ('failed', 'Fallido'),
]


class EmailRecord(models.Model):
    template_base = models.ForeignKey(
        TemplateBase,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='records',
    )
    profile = models.ForeignKey(
        EmailProfile,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='records',
    )
    user = models.ForeignKey(
        'ies.User',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='email_records',
        help_text="Usuario que disparó el envío",
    )
    recipient_email = models.EmailField()
    subject = models.CharField(max_length=200)
    context_data = models.JSONField(
        blank=True,
        null=True,
        help_text="Contexto serializable usado para renderizar",
    )
    send_email = models.BooleanField(
        default=False,
        help_text="¿Se intentó enviar el correo?",
    )
    sent_at = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=EMAIL_STATUS_CHOICES,
        default='pending',
    )
    errors = models.JSONField(blank=True, null=True)
    message_id = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="ID retornado por el servidor SMTP",
    )

    def __str__(self):
        return (
            f"{self.recipient_email} — "
            f"{self.subject[:40]} ({self.status})"
        )

    class Meta:
        ordering = ['-created']
        verbose_name = "Registro de correo"
        verbose_name_plural = "Registros de correos"