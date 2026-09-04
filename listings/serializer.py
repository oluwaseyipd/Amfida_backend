from rest_framework import serializers
from .models import Listing, ListingPhoto, ListingVideo, Amenity, ListingAmenity


class ListingPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingPhoto
        fields = ['id', 'listing', 'listing_image', 'sort_order', 'created_at', 'updated_at']

class ListingVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingVideo
        fields = ['id', 'listing', 'url', 'sort_order', 'created_at', 'updated_at']

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']

class ListingAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingAmenity
        fields = ['id', 'listing', 'amenity_listings', 'created_at', 'updated_at']


class ListingSerializer(serializers.ModelSerializer):

    images = ListingPhotoSerializer(many=True, read_only=True)
    videos = ListingVideoSerializer(many=True, read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)

    class Meta:
        model = Listing
        fields = ['id', 'title', 'description', 'price', 'location', 'status', 'agent', 'hostel', 'amenities', 'images', 'videos', 'created_at', 'updated_at']