from rest_framework import status

from apps.account.test.test_base_class import AccountApiTest


class ActivateAPITest(AccountApiTest):
    def test_successful_activation(self):
        url_for_activation = (
            f'{self.activate_url}?u={self.inactive_user.activation_code}'
        )
        response = self.client.get(url_for_activation)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('msg', response.data)

        self.inactive_user.refresh_from_db()
        self.assertTrue(self.inactive_user.is_active)
        self.assertEqual(self.inactive_user.activation_code, '')

    def test_invalid_activation_code(self):
        url_for_activation = (
            f'{self.activate_url}?u=invalid'
        )
        response = self.client.get(url_for_activation)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)