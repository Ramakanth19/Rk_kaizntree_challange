# accounts/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import LoginSerializer, registerSerializer
from django.conf import settings

class AccountsAPITestCase(TestCase):
    def setUp(self):
        # Setup for test case; creates a user and obtains authentication token for API calls.
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword123')
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.api_key = settings.API_KEY

    def test_login(self):
        # Tests user login functionality, expecting a token in response for valid credentials.
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpassword123'}
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_forgot_password(self):
        # Tests the password reset request flow by sending an email to the user's email address.
        url = reverse('forgot-password')
        data = {'email': 'test@example.com'}
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Password reset email sent.")

    def test_reset_password(self):
        # Tests the actual password reset functionality, ensuring the password is changed successfully.
        user = User.objects.get(username='testuser')
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        url = reverse('reset-password')
        data = {'uid': uid, 'token': token, 'newPassword': 'newpassword123'}
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Password has been reset successfully.")

    def test_create_user(self):
        # Tests the user creation endpoint, verifying the user is successfully created in the database.
        url = reverse('account-create')
        data = {'username': 'newuser', 'password': 'newpassword123', 'email': 'new@example.com'}
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_logout(self):
        # Tests the logout functionality, ensuring the session is terminated successfully.
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('logout')
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertTrue(response_data["success"])

    def test_total_categories(self):
        # Tests the endpoint that returns the total number of categories in the database.
        url = reverse('total-categories')
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_categories', response.data)

    def test_total_items(self):
        # Tests the endpoint that returns the total number of items in the database.
        url = reverse('total-items')
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_items', response.data)