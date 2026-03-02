---
name: send-email
description: Sending emails, creating email templates, and checking email records. Use this skill whenever the user wants to send an email programmatically, create or register a new email template, and related settings.
---

# send-email

Email sending in this project is handled by `email_send/service.py` using Django's built-in SMTP backend. No extra packages required.

## App structure
```
email_send/
├── models.py     # EmailProfile, TemplateBase, EmailRecord
├── service.py    # send_template_email, send_simple_email
├── admin.py      # Admin registration
└── tests.py      # Tests for all functions
```

## Key models

**EmailProfile** — stores SMTP config for Gmail or Outlook.
- Passwords are NEVER stored in the DB; `password_env_var` holds only the env var *name*
- `provider`: `'gmail'` or `'outlook'` (host is set automatically)
- `is_default=True`: used when a template has no linked profile

**TemplateBase** — points to a Django HTML template file.
- `name`: path relative to templates dir (e.g. `email/invitation.html`)
- `subject`: supports `{{ variable }}` syntax
- `profile`: optional FK to EmailProfile; falls back to default

**EmailRecord** — auto-created on every send attempt.
- Always check `record.status`: `'sent'` | `'failed'` | `'pending'`
- `record.errors` contains the exception message on failure

## Sending emails

### With a template
```python
from email_send.models import TemplateBase
from email_send.service import send_template_email

template = TemplateBase.objects.get(name='email/invitation.html')
record = send_template_email(
    template=template,
    recipient_email='user@example.com',
    context={'institution': 'UNAM', 'token': 'abc123'},
    user=request.user,  # optional
)
if record.status == 'failed':
    print(record.errors)
```

### Quick one-off (no template)
```python
from email_send.service import send_simple_email

record = send_simple_email(
    recipient_email='admin@example.com',
    subject='Alerta del sistema',
    html_body='<p>Se detectó un error.</p>',
)
```

### Override the default profile
```python
from email_send.models import EmailProfile
from email_send.service import send_template_email

outlook = EmailProfile.objects.get(provider='outlook')
record = send_template_email(
    template=template,
    recipient_email='user@example.com',
    context={},
    profile=outlook,
)
```

## Creating a new template

1. Create the HTML file: `templates/email/my_template.html`
2. Register it:
```python
from email_send.models import TemplateBase
TemplateBase.objects.create(
    name='email/my_template.html',
    subject='Asunto del correo',
    description='Descripción opcional',
    # profile=... optional, omit to use default
)
```

## Environment variables

Add to `.env` — `password_env_var` stores only the variable *name*, never the secret itself:
```
EMAIL_GMAIL_USER=system@gmail.com
EMAIL_GMAIL_PASSWORD=your_app_password_here

EMAIL_OUTLOOK_USER=system@institution.edu.mx
EMAIL_OUTLOOK_PASSWORD=your_password_here
```

## Running tests
```bash
pytest email_send/tests.py -v
```

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| "No email profile" error | No active `EmailProfile` in DB |
| `SMTPAuthenticationError` | Wrong password or app token |
| Gmail SMTP blocked | Use an App Password, not your account password |
| Outlook 535 5.7.139 | Account may require OAuth2 / Modern Auth |