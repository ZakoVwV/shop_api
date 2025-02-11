from token import EQUAL
from turtledemo.sorting_animate import start_ssort
from unittest.mock import patch

from django.contrib.auth import get_user_model
from rest_framework import status

from apps.account.test.factory import UserFactory
from apps.account.test.test_base_class import AccountApiTest
from apps.account.tasks import send_activation_email_task
from apps.account.test.factory import UserFactory

User = get_user_model()

class RegisterAPITest(AccountApiTest):
    @patch('apps.account.tasks.send_activation_email_task.apply_async')
    def test_register_successful(self, mock_send_mail):
        response = self.client.post(self.register_url, self.default_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_send_mail.assert_called_once()

    def test_register_missing_fields(self):
        missing_fields = {'email', 'last_name', 'first_name', 'password'}
        data_with_missing_fields = UserFactory.generate_user_with_missing_fields(missing_fields)
        response = self.client.post(self.register_url, data_with_missing_fields)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(
            missing_fields.issubset(response.data.keys()),
        )

    def test_invalid_email(self):
        user_data = {
            'email': 'invalid',
            'last_name': 'test',
            'first_name': 'test',
            'password': 'password123',
            'password_confirm': 'password123'
        }
        response = self.client.post(self.register_url, user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_email(self):
        response = self.client.post(self.register_url, self.default_existing_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
