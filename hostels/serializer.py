from rest_framework import serializers
from .models import Area, Hostel


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'name', 'created_at', 'updated_at']

class HostelSerializer(serializers.ModelSerializer):
    area = AreaSerializer(read_only=True)

    class Meta:
        model = Hostel
        fields = ['id', 'name', 'location', 'description', 'area', 'landlord', 'profile_avatar', 'profile_banner', 'created_at', 'updated_at']