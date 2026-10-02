from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthenticationTests(APITestCase):
    """Тесты регистрации и аутентификации."""

    def test_user_can_register(self):
        response = self.client.post(
            '/api/auth/register/',
            {
                'username': 'newuser',
                'password': 'strongpassword123',
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertTrue(
            User.objects.filter(
                username='newuser'
            ).exists()
        )

    def test_password_is_hashed_after_registration(self):
        self.client.post(
            '/api/auth/register/',
            {
                'username': 'newuser',
                'password': 'strongpassword123',
            },
        )

        user = User.objects.get(
            username='newuser'
        )

        self.assertNotEqual(
            user.password,
            'strongpassword123',
        )
        self.assertTrue(
            user.check_password(
                'strongpassword123'
            )
        )

    def test_user_can_get_jwt_tokens(self):
        User.objects.create_user(
            username='testuser',
            password='testpassword123',
        )

        response = self.client.post(
            '/api/auth/token/',
            {
                'username': 'testuser',
                'password': 'testpassword123',
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_authenticated_user_can_get_current_user(self):
        user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
        )

        self.client.force_authenticate(
            user=user,
        )

        response = self.client.get(
            '/api/auth/me/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data['username'],
            'testuser',
        )

    def test_anonymous_user_cannot_get_current_user(self):
        response = self.client.get(
            '/api/auth/me/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )