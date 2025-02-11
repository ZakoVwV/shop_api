
from django.urls import reverse

from rest_framework.test import APITestCase
from apps.account.models import UserResetPasswordToken
from django.contrib.auth import get_user_model
from apps.generals import generate_reset_token
from apps.account.test.factory import UserFactory
from apps.generals.generate_reset_token import generate_reset_password_token
from django.utils import timezone
User = get_user_model()

class AccountApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.register_url = reverse('register')
        cls.activate_url = reverse('activate')
        cls.login_url = reverse('login')
        cls.refresh_token_utl = reverse('refresh-token')
        cls.logout_url = reverse('logout')
        cls.reset_password_url = reverse('reset-password')
        cls.reset_password_confirm_url = reverse('reset-password-confirm')

        cls.user_in_db = User.objects.create(
            email='amirzakov9@gmail.com',
            first_name='test',
            last_name='test',
            password='password123'
        )

        cls.default_user_data = {
            'email': 'test@gmail.com',
            'first_name': 'test',
            'last_name': 'test',
            'password': '123456789',
            'password_confirm': '123456789'
        }
        cls.default_existing_user_data = {
            'email': 'amirzakov9@gmail.com',
            'first_name': 'test',
            'last_name': 'test',
            'password': '123456789',
            'password_confirm': '123456789'
        }

        cls.active_user = UserFactory.create(is_active=True)
        cls.inactive_user = UserFactory.create()

    def generate_reset_password_data(self, user):
        reset_code = UserResetPasswordToken.objects.create(
            user=user,
            token=generate_reset_password_token(),
            created_at=timezone.now()
        )
        return {
            'new_password': 'password123321',
            'new_password_confirm': 'password123321',
            'code': reset_code.token
        }