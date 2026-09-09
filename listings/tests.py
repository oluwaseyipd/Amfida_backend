from decimal import Decimal
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User, AgentProfile, LandLordProfile
from hostels.models import Area, Hostel
from .models import Listing, Amenity, ListingPhoto, ListingVideo


class ListingTests(APITestCase):
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

        self.other_agent_user = User.objects.create_user(
            email='other_agent@test.com',
            first_name='Bob',
            last_name='Broker',
            phone_number='+2348033333333',
            password='TestPassword123!',
        )
        self.other_agent_profile = AgentProfile.objects.get_or_create(user=self.other_agent_user)[0]

        self.area = Area.objects.create(name='Campus East')
        self.hostel = Hostel.objects.create(
            name='Elite Hall',
            location='Campus East Gate',
            description='Prime student hostel',
            area=self.area,
            landlord=self.landlord_profile
        )

        self.amenity1 = Amenity.objects.create(name='WiFi', description='High speed fiber')
        self.amenity2 = Amenity.objects.create(name='Water Heater', description='Constant hot water')

        self.listing = Listing.objects.create(
            title='Single Room Self-Contained',
            description='Ensuite bathroom with kitchen cabinet',
            price=Decimal('180000.00'),
            location='Campus East Gate',
            status='active',
            agent=self.agent_profile,
            hostel=self.hostel
        )
        self.listing.amenities.add(self.amenity1)

    def test_amenity_list(self):
        url = reverse('amenity-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_listing_with_amenities(self):
        url = reverse('create-listing')
        self.client.force_authenticate(user=self.agent_user)
        data = {
            'title': 'Double Room Suite',
            'description': 'Spacious double room for two students',
            'price': '300000.00',
            'location': 'Campus East Gate',
            'status': 'active',
            'hostel': self.hostel.id,
            'amenity_ids': [self.amenity1.id, self.amenity2.id]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['amenities']), 2)

    def test_listing_update_permissions(self):
        url = reverse('update-listing', kwargs={'pk': self.listing.pk})
        
        # Unauthorized competitor tries to edit
        self.client.force_authenticate(user=self.other_agent_user)
        res_forbidden = self.client.put(url, {
            'title': 'Hacked Listing',
            'description': 'Hacked',
            'price': '1.00',
            'location': 'Nowhere',
            'hostel': self.hostel.id
        })
        self.assertEqual(res_forbidden.status_code, status.HTTP_403_FORBIDDEN)

        # Owner agent edits
        self.client.force_authenticate(user=self.agent_user)
        res_owner = self.client.put(url, {
            'title': 'Single Room Self-Contained (Upgraded)',
            'description': 'Ensuite bathroom with newly painted interior',
            'price': '190000.00',
            'location': 'Campus East Gate',
            'hostel': self.hostel.id,
            'amenity_ids': [self.amenity2.id]
        })
        self.assertEqual(res_owner.status_code, status.HTTP_200_OK)
        self.assertEqual(res_owner.data['title'], 'Single Room Self-Contained (Upgraded)')
        self.assertEqual(len(res_owner.data['amenities']), 1)

    def test_listing_photo_upload_and_delete(self):
        url = reverse('listing-photos', kwargs={'pk': self.listing.pk})
        
        dummy_img = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff'
            b'\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00'
            b'\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
        )
        photo_file = SimpleUploadedFile('room.gif', dummy_img, content_type='image/gif')
        
        self.client.force_authenticate(user=self.agent_user)
        res_upload = self.client.post(url, {'listing_image': photo_file, 'sort_order': 1}, format='multipart')
        self.assertEqual(res_upload.status_code, status.HTTP_201_CREATED)
        photo_id = res_upload.data['id']

        # Delete photo
        del_url = reverse('delete-listing-photo', kwargs={'pk': photo_id})
        res_del = self.client.delete(del_url)
        self.assertEqual(res_del.status_code, status.HTTP_204_NO_CONTENT)

    def test_listing_filter_and_search(self):
        url = reverse('listing-list')
        response = self.client.get(f'{url}?search=Self-Contained&price__lte=200000')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)
