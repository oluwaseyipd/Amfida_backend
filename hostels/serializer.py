from rest_framework import serializers
from .models import Area, Hostel


class AreaSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, trim_whitespace=True)

    class Meta:
        model = Area
        fields = ['id', 'name', 'created_at', 'updated_at']

    def validate_name(self, value):
        normalized_name = ' '.join(value.split())
        queryset = Area.objects.filter(name__iexact=normalized_name)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError('An area with this name already exists.')
        return normalized_name

class HostelSerializer(serializers.ModelSerializer):
    area = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all())
    landlord = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Hostel
        fields = ['id', 'name', 'location', 'description', 'area', 'landlord', 'profile_avatar', 'profile_banner', 'created_at', 'updated_at']