from decimal import Decimal
from rest_framework import serializers
from .models import Listing, ListingPhoto, ListingVideo, Amenity, ListingAmenity


class ListingPhotoSerializer(serializers.ModelSerializer):
    sort_order = serializers.IntegerField(min_value=0, default=0, required=False)
    listing = serializers.PrimaryKeyRelatedField(queryset=Listing.objects.all(), required=False)

    class Meta:
        model = ListingPhoto
        fields = ['id', 'listing', 'listing_image', 'sort_order', 'created_at', 'updated_at']


class ListingVideoSerializer(serializers.ModelSerializer):
    sort_order = serializers.IntegerField(min_value=0, default=0, required=False)
    listing = serializers.PrimaryKeyRelatedField(queryset=Listing.objects.all(), required=False)

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
        fields = ['id', 'listing', 'amenity', 'created_at', 'updated_at']


class ListingSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.01'))
    agent = serializers.PrimaryKeyRelatedField(read_only=True)
    images = ListingPhotoSerializer(many=True, read_only=True)
    videos = ListingVideoSerializer(many=True, read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    amenity_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Amenity.objects.all(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'price', 'location', 'status',
            'agent', 'hostel', 'amenities', 'amenity_ids', 'images', 'videos',
            'created_at', 'updated_at'
        ]

    def create(self, validated_data):
        amenities_data = validated_data.pop('amenity_ids', None)
        listing = Listing.objects.create(**validated_data)
        if amenities_data is not None:
            listing.amenities.set(amenities_data)
        return listing

    def update(self, instance, validated_data):
        amenities_data = validated_data.pop('amenity_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if amenities_data is not None:
            instance.amenities.set(amenities_data)
        return instance