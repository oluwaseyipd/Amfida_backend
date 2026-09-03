from django.db import models

from accounts.models import Agent
from hostels.models import Hostel, Area



class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    video_url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=50, default='active')
    agent = models.ForeignKey('accounts.Agent', on_delete=models.CASCADE, related_name='listings')
    hostel = models.ForeignKey('hostels.Hostel', on_delete=models.CASCADE, related_name='listings')
    area = models.ForeignKey('hostels.Area', on_delete=models.CASCADE, related_name='listings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ListingPhoto(models.Model):
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='images')
    url = models.URLField()
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Image for {self.listing.title} - Order: {self.sort_order}"


class ListingVideo(models.Model):
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='videos')
    url = models.URLField()
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Video for {self.listing.title} - Order: {self.sort_order}"


class Amenity(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ListingAmenity(models.Model):
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='amenities')
    amenity = models.ForeignKey('Amenity', on_delete=models.CASCADE, related_name='listing_amenities')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.amenity.name} for {self.listing.title}"