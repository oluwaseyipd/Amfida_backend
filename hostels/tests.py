from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User, LandLordProfile, AgentProfile
from .models import Area, Hostel


class HostelTests(APITestCase):
    def setUp(self):
        self.landlord_user = User.objects.create_user(
            email='landlord@test.com',
            first_name='Leo',
            last_name='Landlord',
            phone_number='+2348011111111',
            password='TestPassword123!',
        )
        self.landlord_profile = LandLordProfile.objects.get_or_create(user=self.landlord_user)[0]

        self.other_landlord_user = User.objects.create_user(
            email='other_landlord@test.com',
            first_name='Oscar',
            last_name='Other',
            phone_number='+2348022222222',
            password='TestPassword123!',
        )
        self.other_landlord_profile = LandLordProfile.objects.get_or_create(user=self.other_landlord_user)[0]

        self.admin_user = User.objects.create_superuser(
            email='admin@test.com',
            first_name='Admin',
            last_name='Root',
            phone_number='+2348033333333',
            password='AdminPassword123!',
        )

        self.area = Area.objects.create(name='Campus West')
        self.hostel = Hostel.objects.create(
            name='Royal Palms',
            location='Campus West Gate',
            description='Executive student suites',
            area=self.area,
            landlord=self.landlord_profile
        )

    def test_area_list(self):
        url = reverse('area-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_area_create_admin_only(self):
        url = reverse('create-area')
        self.client.force_authenticate(user=self.landlord_user)
        res_forbidden = self.client.post(url, {'name': 'Campus North'})
        self.assertEqual(res_forbidden.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.admin_user)
        res_admin = self.client.post(url, {'name': 'Campus North'})
        self.assertEqual(res_admin.status_code, status.HTTP_201_CREATED)

    def test_hostel_create(self):
        url = reverse('create-hostel')
        self.client.force_authenticate(user=self.landlord_user)
        data = {
            'name': 'Silver Crest Lodge',
            'location': 'Behind Sport Complex',
            'description': 'Quiet environment for serious students',
            'area': self.area.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['landlord'], self.landlord_profile.id)

    def test_hostel_list_and_search(self):
        url = reverse('hostel-list')
        response = self.client.get(f'{url}?search=Royal')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)

    def test_hostel_update_permission(self):
        url = reverse('update-hostel', kwargs={'pk': self.hostel.pk})
        # Competitor landlord tries to update
        self.client.force_authenticate(user=self.other_landlord_user)
        res_attack = self.client.put(url, {
            'name': 'Hacked Hostel Name',
            'location': 'Nowhere',
            'description': 'Hacked',
            'area': self.area.id
        })
        self.assertEqual(res_attack.status_code, status.HTTP_403_FORBIDDEN)

        # Owner landlord updates
        self.client.force_authenticate(user=self.landlord_user)
        res_owner = self.client.put(url, {
            'name': 'Royal Palms Luxury suites',
            'location': 'Campus West Gate',
            'description': 'Upgraded executive suites',
            'area': self.area.id
        })
        self.assertEqual(res_owner.status_code, status.HTTP_200_OK)
        self.assertEqual(res_owner.data['name'], 'Royal Palms Luxury suites')
