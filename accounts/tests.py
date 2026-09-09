from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, LandLordProfile, AgentProfile


class AccountTests(APITestCase):
    def setUp(self):
        self.landlord_user = User.objects.create_user(
            email='landlord@test.com',
            first_name='Leo',
            last_name='Landlord',
            phone_number='+2348011111111',
            password='TestPassword123!',
        )
        LandLordProfile.objects.get_or_create(user=self.landlord_user)

        self.agent_user = User.objects.create_user(
            email='agent@test.com',
            first_name='Amy',
            last_name='Agent',
            phone_number='+2348022222222',
            password='TestPassword123!',
        )
        AgentProfile.objects.get_or_create(user=self.agent_user)

        self.admin_user = User.objects.create_superuser(
            email='admin@test.com',
            first_name='Admin',
            last_name='Root',
            phone_number='+2348033333333',
            password='AdminPassword123!',
        )

    def test_register_landlord(self):
        url = reverse('create_user')
        data = {
            'email': 'new_landlord@test.com',
            'first_name': 'New',
            'last_name': 'Landlord',
            'phone_number': '+2348044444444',
            'password': 'StrongPassword123!',
            'role': 'landlord'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['role'], 'landlord')
        user = User.objects.get(email='new_landlord@test.com')
        self.assertTrue(hasattr(user, 'landlord_profile'))

    def test_register_agent(self):
        url = reverse('create_user')
        data = {
            'email': 'new_agent@test.com',
            'first_name': 'New',
            'last_name': 'Agent',
            'phone_number': '+2348055555555',
            'password': 'StrongPassword123!',
            'role': 'agent'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['role'], 'agent')
        user = User.objects.get(email='new_agent@test.com')
        self.assertTrue(hasattr(user, 'agent_profile'))

    def test_jwt_login(self):
        url = reverse('token_obtain_pair')
        data = {
            'email': 'landlord@test.com',
            'password': 'TestPassword123!',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_me_unauthenticated(self):
        url = reverse('user_me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_me_authenticated(self):
        url = reverse('user_me')
        self.client.force_authenticate(user=self.agent_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'agent@test.com')
        self.assertEqual(response.data['role'], 'agent')

    def test_user_me_patch(self):
        url = reverse('user_me')
        self.client.force_authenticate(user=self.agent_user)
        response = self.client.patch(url, {'first_name': 'Amelia'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Amelia')
        self.agent_user.refresh_from_db()
        self.assertEqual(self.agent_user.first_name, 'Amelia')

    def test_admin_user_list(self):
        url = reverse('user_list')
        self.client.force_authenticate(user=self.landlord_user)
        res_forbidden = self.client.get(url)
        self.assertEqual(res_forbidden.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.admin_user)
        res_admin = self.client.get(url)
        self.assertEqual(res_admin.status_code, status.HTTP_200_OK)
