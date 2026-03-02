"""
Tests for the full password recovery flow.

Flow:
  1. POST /api/password-recovery/          → request email
  2. GET  /api/password-recovery/{key}/    → validate token
  3. POST /api/password-recovery/{key}/confirm/ → set new password
                                              + returns UserDataSerializer
"""
from datetime import timedelta
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from ies.models import User, PasswordRecoveryToken


# ── Helpers ───────────────────────────────────────────────────────────────

def make_user(**kwargs):
    defaults = dict(
        username='testuser',
        email='test@example.com',
        is_active=True,
    )
    defaults.update(kwargs)
    user = User(**defaults)
    user.set_password('initial_pass_123')
    user.save()
    return user


def make_token(user, expired=False, used=False):
    token = PasswordRecoveryToken(user=user)
    token.save()
    if expired:
        token.expires_at = timezone.now() - timedelta(hours=1)
        token.save()
    if used:
        token.mark_used()
    return token


URL_REQUEST = reverse('password_recovery_request')


def url_validate(key):
    return reverse('password_recovery_validate', args=[key])


def url_confirm(key):
    return reverse('password_recovery_confirm', args=[key])


# ── PasswordRecoveryToken model ───────────────────────────────────────────

class PasswordRecoveryTokenModelTest(TestCase):

    def setUp(self):
        self.user = make_user()

    def test_expires_at_set_automatically(self):
        token = PasswordRecoveryToken.objects.create(user=self.user)
        self.assertIsNotNone(token.expires_at)
        delta = token.expires_at - token.created_at
        expected = timedelta(hours=PasswordRecoveryToken.EXPIRY_HOURS)
        self.assertAlmostEqual(
            delta.total_seconds(),
            expected.total_seconds(),
            delta=5,
        )

    def test_is_valid_new_token(self):
        token = PasswordRecoveryToken.objects.create(user=self.user)
        self.assertTrue(token.is_valid())

    def test_is_valid_expired_token(self):
        token = make_token(self.user, expired=True)
        self.assertFalse(token.is_valid())

    def test_is_valid_used_token(self):
        token = make_token(self.user, used=True)
        self.assertFalse(token.is_valid())

    def test_mark_used_sets_used_at(self):
        token = PasswordRecoveryToken.objects.create(user=self.user)
        self.assertIsNone(token.used_at)
        token.mark_used()
        self.assertIsNotNone(token.used_at)
        self.assertFalse(token.is_valid())

    def test_str_includes_email(self):
        token = PasswordRecoveryToken.objects.create(user=self.user)
        self.assertIn(self.user.email, str(token))


# ── POST /api/password-recovery/ ─────────────────────────────────────────

class PasswordRecoveryRequestViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = make_user()

    @patch('api.views.auth.recovery_views._send_recovery_email')
    def test_existing_email_creates_token_and_sends(
        self, mock_send
    ):
        resp = self.client.post(
            URL_REQUEST, {'email': self.user.email}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(
            PasswordRecoveryToken.objects.filter(
                user=self.user
            ).exists()
        )
        mock_send.assert_called_once()

    def test_nonexistent_email_returns_200_no_token(self):
        """Must not reveal whether the email exists."""
        resp = self.client.post(
            URL_REQUEST, {'email': 'nobody@example.com'}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn('detail', resp.data)
        self.assertEqual(
            PasswordRecoveryToken.objects.count(), 0
        )

    @patch('api.views.auth.recovery_views._send_recovery_email')
    def test_inactive_user_ignored(self, mock_send):
        self.user.is_active = False
        self.user.save()
        resp = self.client.post(
            URL_REQUEST, {'email': self.user.email}
        )
        self.assertEqual(resp.status_code, 200)
        mock_send.assert_not_called()

    def test_missing_email_returns_400(self):
        resp = self.client.post(URL_REQUEST, {})
        self.assertEqual(resp.status_code, 400)

    @patch('api.views.auth.recovery_views._send_recovery_email')
    def test_previous_tokens_invalidated_on_new_request(
        self, mock_send
    ):
        old_token = PasswordRecoveryToken.objects.create(
            user=self.user
        )
        self.assertIsNone(old_token.used_at)

        self.client.post(
            URL_REQUEST, {'email': self.user.email}
        )

        old_token.refresh_from_db()
        self.assertIsNotNone(old_token.used_at)
        # A new token must have been created
        self.assertEqual(
            PasswordRecoveryToken.objects.filter(
                user=self.user, used_at__isnull=True
            ).count(),
            1,
        )

    @patch('api.views.auth.recovery_views._send_recovery_email')
    def test_email_case_insensitive(self, mock_send):
        resp = self.client.post(
            URL_REQUEST,
            {'email': self.user.email.upper()},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(
            PasswordRecoveryToken.objects.filter(
                user=self.user
            ).exists()
        )


# ── GET /api/password-recovery/{key}/ ────────────────────────────────────

class PasswordRecoveryValidateViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = make_user()

    def test_valid_token_returns_user_info(self):
        token = make_token(self.user)
        resp = self.client.get(url_validate(token.key))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['email'], self.user.email)
        self.assertTrue(resp.data['valid'])

    def test_expired_token_returns_400(self):
        token = make_token(self.user, expired=True)
        resp = self.client.get(url_validate(token.key))
        self.assertEqual(resp.status_code, 400)

    def test_used_token_returns_400(self):
        token = make_token(self.user, used=True)
        resp = self.client.get(url_validate(token.key))
        self.assertEqual(resp.status_code, 400)

    def test_invalid_key_returns_404(self):
        import uuid
        resp = self.client.get(
            url_validate(uuid.uuid4())
        )
        self.assertEqual(resp.status_code, 404)

    def test_validate_does_not_consume_token(self):
        token = make_token(self.user)
        self.client.get(url_validate(token.key))
        token.refresh_from_db()
        self.assertIsNone(token.used_at)


# ── POST /api/password-recovery/{key}/confirm/ ───────────────────────────

class PasswordRecoveryConfirmViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = make_user()

    def test_valid_confirm_changes_password(self):
        token = make_token(self.user)
        resp = self.client.post(url_confirm(token.key), {
            'password': 'new_secure_pass',
            'password_confirm': 'new_secure_pass',
        })
        self.assertEqual(resp.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(
            self.user.check_password('new_secure_pass')
        )

    def test_valid_confirm_marks_token_used(self):
        token = make_token(self.user)
        self.client.post(url_confirm(token.key), {
            'password': 'new_secure_pass',
            'password_confirm': 'new_secure_pass',
        })
        token.refresh_from_db()
        self.assertIsNotNone(token.used_at)

    def test_valid_confirm_sets_password_changed_flag(self):
        token = make_token(self.user)
        self.client.post(url_confirm(token.key), {
            'password': 'new_secure_pass',
            'password_confirm': 'new_secure_pass',
        })
        self.user.refresh_from_db()
        self.assertTrue(self.user.password_changed)

    def test_confirm_returns_user_data_serializer(self):
        """Response must include token and user fields (auto-login)."""
        token = make_token(self.user)
        resp = self.client.post(url_confirm(token.key), {
            'password': 'new_secure_pass',
            'password_confirm': 'new_secure_pass',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertIn('token', resp.data)
        self.assertIn('email', resp.data)
        self.assertIn('id', resp.data)
        # Token must not be empty
        self.assertIsNotNone(resp.data['token'])

    def test_expired_token_returns_400(self):
        token = make_token(self.user, expired=True)
        resp = self.client.post(url_confirm(token.key), {
            'password': 'new_secure_pass',
            'password_confirm': 'new_secure_pass',
        })
        self.assertEqual(resp.status_code, 400)

    def test_used_token_returns_400(self):
        token = make_token(self.user, used=True)
        resp = self.client.post(url_confirm(token.key), {
            'password': 'new_secure_pass',
            'password_confirm': 'new_secure_pass',
        })
        self.assertEqual(resp.status_code, 400)

    def test_invalid_key_returns_404(self):
        import uuid
        resp = self.client.post(
            url_confirm(uuid.uuid4()),
            {'password': 'x', 'password_confirm': 'x'},
        )
        self.assertEqual(resp.status_code, 404)

    def test_passwords_mismatch_returns_400(self):
        token = make_token(self.user)
        resp = self.client.post(url_confirm(token.key), {
            'password': 'new_secure_pass',
            'password_confirm': 'different_pass',
        })
        self.assertEqual(resp.status_code, 400)
        self.assertIn('password_confirm', resp.data['errors'])

    def test_short_password_returns_400(self):
        token = make_token(self.user)
        resp = self.client.post(url_confirm(token.key), {
            'password': 'short',
            'password_confirm': 'short',
        })
        self.assertEqual(resp.status_code, 400)
        self.assertIn('password', resp.data['errors'])

    def test_missing_password_returns_400(self):
        token = make_token(self.user)
        resp = self.client.post(url_confirm(token.key), {})
        self.assertEqual(resp.status_code, 400)

    def test_used_token_cannot_be_reused(self):
        """Confirm twice with same token must fail on second attempt."""
        token = make_token(self.user)
        payload = {
            'password': 'new_secure_pass',
            'password_confirm': 'new_secure_pass',
        }
        resp1 = self.client.post(url_confirm(token.key), payload)
        resp2 = self.client.post(url_confirm(token.key), payload)
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 400)