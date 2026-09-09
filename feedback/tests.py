from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User, AgentProfile, LandLordProfile
from hostels.models import Area, Hostel
from listings.models import Listing
from .models import Review, Report


class FeedbackTests(APITestCase):
    def setUp(self):
        self.landlord_user = User.objects.create_user(
            email='landlord@test.com',
            first_name='Leo',
            last_name='Landlord',
            phone_number='+2348011111111',
            password='TestPassword123!',
        )
        self.landlord_profile = LandLordProfile.objects.get_or_create(user=self.landlord_user)[0]

        self.agent_user = User.objects.create_user(
            email='agent@test.com',
            first_name='Amy',
            last_name='Agent',
            phone_number='+2348022222222',
            password='TestPassword123!',
        )
        self.agent_profile = AgentProfile.objects.get_or_create(user=self.agent_user)[0]

        self.admin_user = User.objects.create_superuser(
            email='admin@test.com',
            first_name='Admin',
            last_name='Root',
            phone_number='+2348033333333',
            password='AdminPassword123!',
        )

        self.area = Area.objects.create(name='Campus South')
        self.hostel = Hostel.objects.create(
            name='Greenwood Lodge',
            location='Campus South Gate',
            description='Affordable suites',
            area=self.area,
            landlord=self.landlord_profile
        )

        self.listing = Listing.objects.create(
            title='Standard Room',
            description='Affordable standard room',
            price=Decimal('120000.00'),
            location='Campus South Gate',
            agent=self.agent_profile,
            hostel=self.hostel
        )

    def test_open_review_creation_and_filtering(self):
        url = reverse('review-list')
        data = {
            'listing': self.listing.id,
            'name': 'Student Prospect',
            'rating': 5,
            'comment': 'Clean hostel and very close to the lecture halls.'
        }
        # Anonymous visitor posts a review
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Anonymous visitor queries reviews for this listing
        res_list = self.client.get(f'{url}?listing={self.listing.id}')
        self.assertEqual(res_list.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_list.data), 1)
        self.assertEqual(res_list.data[0]['name'], 'Student Prospect')

    def test_open_report_creation(self):
        url = reverse('report-list')
        data = {
            'listing': self.listing.id,
            'name': 'Whistleblower Student',
            'reason': 'Listing price mismatch on site inspection',
            'contact_info': 'student@uni.edu'
        }
        # Anonymous visitor reports an issue
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_report_list_admin_only(self):
        url = reverse('report-list')
        # Anonymous access is blocked
        res_anon = self.client.get(url)
        self.assertEqual(res_anon.status_code, status.HTTP_401_UNAUTHORIZED)

        # Regular user access is blocked
        self.client.force_authenticate(user=self.landlord_user)
        res_forbidden = self.client.get(url)
        self.assertEqual(res_forbidden.status_code, status.HTTP_403_FORBIDDEN)

        # Admin access is permitted
        self.client.force_authenticate(user=self.admin_user)
        res_admin = self.client.get(url)
        self.assertEqual(res_admin.status_code, status.HTTP_200_OK)
