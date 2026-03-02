from django.contrib import admin
from .models import EmailProfile, TemplateBase, EmailRecord


@admin.register(EmailProfile)
class EmailProfileAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'provider', 'username',
        'is_default', 'is_active',
    ]
    list_filter = ['provider', 'is_active', 'is_default']
    search_fields = ['name', 'username']
    fieldsets = [
        (None, {
            'fields': [
                'name', 'provider', 'is_active', 'is_default',
            ],
        }),
        ('SMTP', {
            'fields': [
                'host', 'port', 'use_tls', 'use_ssl',
                'username', 'password_env_var',
            ],
        }),
        ('Remitente', {
            'fields': ['from_email', 'from_name'],
        }),
    ]


@admin.register(TemplateBase)
class TemplateBaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'profile', 'created']
    list_filter = ['profile']
    search_fields = ['name', 'subject']


@admin.register(EmailRecord)
class EmailRecordAdmin(admin.ModelAdmin):
    list_display = [
        'recipient_email', 'subject', 'status',
        'profile', 'created',
    ]
    list_filter = ['status', 'profile']
    search_fields = ['recipient_email', 'subject']
    readonly_fields = [
        'recipient_email', 'subject', 'status',
        'errors', 'sent_at', 'created',
        'context_data', 'message_id', 'send_email',
        'template_base', 'profile', 'user',
    ]