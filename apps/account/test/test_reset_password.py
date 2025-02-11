from datetime import timedelta

from unittest.mock import patch

from django.utils.timezone import now

from rest_framework import status

from apps.account.models import UserResetPasswordToken
from apps.account.test.factory import UserFactory
from apps.account.test.test_base_class import AccountApiTest


class AccountPasswordResetTest(AccountApiTest):
    @patch('apps.account.tasks.send_reset_password_email_task.apply_async')
    def test_successful_reset_password(self, mock_send_mail):
        email_data = {'email': self.active_user.email}
        response = self.client.post(self.reset_password_url, email_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_send_mail.assert_called_once()

    def test_non_existent_email(self):
        response = self.client.post(self.reset_password_url, self.default_user_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_successful_reset_password_confirm(self):
        data = self.generate_reset_password_data(self.active_user)
        response = self.client.post(self.reset_password_confirm_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('msg', response.data)

        self.active_user.refresh_from_db()
        self.assertTrue(self.active_user.check_password(data['new_password']))

        with self.assertRaises(
            UserResetPasswordToken.DoesNotExist
        ):
            UserResetPasswordToken.objects.get(token=data['code'])

        response = self.client.post(self.reset_password_confirm_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_reset_code(self):
        data = self.generate_reset_password_data(self.active_user)
        data['code'] = '123'
        response = self.client.post(self.reset_password_confirm_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('msg', response.data)
