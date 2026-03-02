from unittest.mock import patch, MagicMock

from django.test import TestCase

from email_send.models import (
    EmailProfile, TemplateBase, EmailRecord,
)
from email_send.service import (
    send_template_email,
    send_simple_email,
    get_default_profile,
    build_connection,
)


# ---------------------------------------------------------------------------
# EmailProfile
# ---------------------------------------------------------------------------

class EmailProfileModelTest(TestCase):

    def setUp(self):
        self.gmail = EmailProfile.objects.create(
            name='Gmail Test',
            provider='gmail',
            username='test@gmail.com',
            password_env_var='TEST_GMAIL_PASS',
            is_default=True,
            is_active=True,
        )
        self.outlook = EmailProfile.objects.create(
            name='Outlook Test',
            provider='outlook',
            username='test@outlook.com',
            password_env_var='TEST_OUTLOOK_PASS',
            is_active=True,
        )

    def test_gmail_uses_preset_host(self):
        self.assertEqual(
            self.gmail.get_host(), 'smtp.gmail.com'
        )

    def test_outlook_uses_preset_host(self):
        self.assertEqual(
            self.outlook.get_host(), 'smtp.office365.com'
        )

    def test_custom_host_overrides_preset(self):
        self.gmail.host = 'custom.smtp.example.com'
        self.assertEqual(
            self.gmail.get_host(), 'custom.smtp.example.com'
        )

    def test_get_password_reads_env_var(self):
        with patch.dict('os.environ', {'TEST_GMAIL_PASS': 'secret'}):
            self.assertEqual(self.gmail.get_password(), 'secret')

    def test_get_password_missing_var_returns_empty_string(self):
        self.assertEqual(self.gmail.get_password(), '')

    def test_get_from_email_falls_back_to_username(self):
        self.assertEqual(
            self.gmail.get_from_email(), 'test@gmail.com'
        )

    def test_get_from_email_uses_explicit_from_email(self):
        self.gmail.from_email = 'noreply@example.com'
        self.assertEqual(
            self.gmail.get_from_email(), 'noreply@example.com'
        )

    def test_get_from_header_without_name(self):
        self.assertEqual(
            self.gmail.get_from_header(), 'test@gmail.com'
        )

    def test_get_from_header_with_from_name(self):
        self.gmail.from_name = 'Sistema ONIGIES'
        header = self.gmail.get_from_header()
        self.assertIn('Sistema ONIGIES', header)
        self.assertIn('test@gmail.com', header)

    def test_str_includes_name_and_provider(self):
        self.assertIn('Gmail Test', str(self.gmail))
        self.assertIn('Gmail', str(self.gmail))


# ---------------------------------------------------------------------------
# get_default_profile
# ---------------------------------------------------------------------------

class GetDefaultProfileTest(TestCase):

    def test_returns_none_when_no_profiles(self):
        self.assertIsNone(get_default_profile())

    def test_returns_default_profile(self):
        profile = EmailProfile.objects.create(
            name='Default',
            provider='gmail',
            username='x@gmail.com',
            password_env_var='VAR',
            is_default=True,
            is_active=True,
        )
        self.assertEqual(get_default_profile(), profile)

    def test_returns_any_active_if_none_is_default(self):
        profile = EmailProfile.objects.create(
            name='Active',
            provider='outlook',
            username='x@outlook.com',
            password_env_var='VAR',
            is_default=False,
            is_active=True,
        )
        self.assertEqual(get_default_profile(), profile)

    def test_skips_inactive_profiles(self):
        EmailProfile.objects.create(
            name='Inactive',
            provider='gmail',
            username='x@gmail.com',
            password_env_var='VAR',
            is_active=False,
        )
        self.assertIsNone(get_default_profile())


# ---------------------------------------------------------------------------
# TemplateBase
# ---------------------------------------------------------------------------

class TemplateBaseModelTest(TestCase):

    def setUp(self):
        self.profile = EmailProfile.objects.create(
            name='Default',
            provider='gmail',
            username='test@gmail.com',
            password_env_var='GMAIL_PASS',
            is_default=True,
            is_active=True,
        )
        self.template = TemplateBase.objects.create(
            name='email/invitation.html',
            subject='Invitación al sistema',
            profile=self.profile,
        )

    def test_str_returns_template_path(self):
        self.assertEqual(
            str(self.template), 'email/invitation.html'
        )

    def test_template_linked_to_profile(self):
        self.assertEqual(self.template.profile, self.profile)

    def test_profile_null_allowed(self):
        t = TemplateBase.objects.create(
            name='email/no_profile.html',
            subject='Sin perfil',
        )
        self.assertIsNone(t.profile)


# ---------------------------------------------------------------------------
# send_template_email
# ---------------------------------------------------------------------------

class SendTemplateEmailTest(TestCase):

    def setUp(self):
        self.profile = EmailProfile.objects.create(
            name='Default',
            provider='gmail',
            username='test@gmail.com',
            password_env_var='GMAIL_PASS',
            is_default=True,
            is_active=True,
        )
        self.template = TemplateBase.objects.create(
            name='email/test.html',
            subject='Hola {{ name }}',
            profile=self.profile,
        )

    @patch('email_send.service.build_connection')
    @patch('email_send.service.render_to_string')
    def test_success_creates_sent_record(
        self, mock_render, mock_conn
    ):
        mock_render.return_value = '<p>Hola Mundo</p>'
        mock_conn.return_value = MagicMock()

        record = send_template_email(
            template=self.template,
            recipient_email='user@example.com',
            context={'name': 'Mundo'},
        )

        self.assertEqual(record.status, 'sent')
        self.assertEqual(
            record.recipient_email, 'user@example.com'
        )
        self.assertIsNotNone(record.sent_at)
        self.assertTrue(record.send_email)

    @patch('email_send.service.build_connection')
    @patch('email_send.service.render_to_string')
    def test_failure_records_error(
        self, mock_render, mock_conn
    ):
        mock_render.return_value = '<p>Hola</p>'
        mock_conn.side_effect = Exception('SMTP refused')

        record = send_template_email(
            template=self.template,
            recipient_email='user@example.com',
            context={},
        )

        self.assertEqual(record.status, 'failed')
        self.assertIn('error', record.errors)
        self.assertIn('SMTP refused', record.errors['error'])

    def test_no_profile_creates_failed_record(self):
        self.profile.delete()
        template = TemplateBase.objects.create(
            name='email/no_profile.html',
            subject='Sin perfil',
        )

        record = send_template_email(
            template=template,
            recipient_email='user@example.com',
            context={},
        )

        self.assertEqual(record.status, 'failed')
        self.assertIn(
            'No email profile', record.errors['error']
        )

    @patch('email_send.service.build_connection')
    @patch('email_send.service.render_to_string')
    def test_profile_override_is_used(
        self, mock_render, mock_conn
    ):
        mock_render.return_value = '<p>Test</p>'
        mock_conn.return_value = MagicMock()

        other = EmailProfile.objects.create(
            name='Outlook',
            provider='outlook',
            username='other@outlook.com',
            password_env_var='OUTLOOK_PASS',
            is_active=True,
        )
        record = send_template_email(
            template=self.template,
            recipient_email='user@example.com',
            context={},
            profile=other,
        )

        self.assertEqual(record.profile, other)

    @patch('email_send.service.build_connection')
    @patch('email_send.service.render_to_string')
    def test_context_stored_in_record(
        self, mock_render, mock_conn
    ):
        mock_render.return_value = '<p>Hi</p>'
        mock_conn.return_value = MagicMock()

        context = {'user': 'Ana', 'year': 2025}
        record = send_template_email(
            template=self.template,
            recipient_email='user@example.com',
            context=context,
        )

        self.assertEqual(record.context_data, context)


# ---------------------------------------------------------------------------
# send_simple_email
# ---------------------------------------------------------------------------

class SendSimpleEmailTest(TestCase):

    def setUp(self):
        self.profile = EmailProfile.objects.create(
            name='Default',
            provider='gmail',
            username='test@gmail.com',
            password_env_var='GMAIL_PASS',
            is_default=True,
            is_active=True,
        )

    @patch('email_send.service.build_connection')
    def test_success_creates_sent_record(self, mock_conn):
        mock_conn.return_value = MagicMock()

        record = send_simple_email(
            recipient_email='user@example.com',
            subject='Test simple',
            html_body='<p>Cuerpo del correo</p>',
        )

        self.assertEqual(record.status, 'sent')
        self.assertEqual(record.subject, 'Test simple')
        self.assertIsNotNone(record.sent_at)

    @patch('email_send.service.build_connection')
    def test_failure_records_error(self, mock_conn):
        mock_conn.side_effect = Exception('Timeout')

        record = send_simple_email(
            recipient_email='user@example.com',
            subject='Fail',
            html_body='<p>Cuerpo</p>',
        )

        self.assertEqual(record.status, 'failed')
        self.assertIn('Timeout', record.errors['error'])

    def test_no_profile_creates_failed_record(self):
        self.profile.delete()

        record = send_simple_email(
            recipient_email='user@example.com',
            subject='Sin perfil',
            html_body='<p>Cuerpo</p>',
        )

        self.assertEqual(record.status, 'failed')

    @patch('email_send.service.build_connection')
    def test_profile_override_is_used(self, mock_conn):
        mock_conn.return_value = MagicMock()

        other = EmailProfile.objects.create(
            name='Outlook',
            provider='outlook',
            username='other@outlook.com',
            password_env_var='OUTLOOK_PASS',
            is_active=True,
        )
        record = send_simple_email(
            recipient_email='user@example.com',
            subject='Test',
            html_body='<p>Cuerpo</p>',
            profile=other,
        )

        self.assertEqual(record.profile, other)


# ---------------------------------------------------------------------------
# EmailRecord
# ---------------------------------------------------------------------------

class EmailRecordModelTest(TestCase):

    def test_str_includes_email_subject_and_status(self):
        record = EmailRecord.objects.create(
            recipient_email='test@example.com',
            subject='Bienvenido al sistema',
            status='sent',
        )
        s = str(record)
        self.assertIn('test@example.com', s)
        self.assertIn('sent', s)

    def test_default_status_is_pending(self):
        record = EmailRecord.objects.create(
            recipient_email='x@example.com',
            subject='Check',
        )
        self.assertEqual(record.status, 'pending')

    def test_default_send_email_is_false(self):
        record = EmailRecord.objects.create(
            recipient_email='x@example.com',
            subject='Check',
        )
        self.assertFalse(record.send_email)