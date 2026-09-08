from rest_framework import serializers
from .models import Report, Review


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        read_only_fields = ["status", "created_at"]
        fields = ['id', 'name', 'listing',  'reason', 'contact_info', 'status', 'created_at']

class ReviewSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Review
        fields = ['id', 'name', 'listing', 'rating', 'comment', 'created_at']