from django.db import models

from accounts.models import LandLord


class Area(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Hostel(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    areas = models.ManyToManyField(Area, related_name='hostels')
    landlord = models.ForeignKey('accounts.LandLord', on_delete=models.CASCADE, related_name='hostels')
    profile_avatar = models.ImageField(upload_to='hostel_profiles/avatars/', blank=True, null=True)
    profile_banner = models.ImageField(upload_to='hostel_profiles/banners/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
