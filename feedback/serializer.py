from rest_framework import serializers
from .models import Report, Review


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'name', 'listing',  'reason', 'contact_info', 'status', 'created_at']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'listing', 'rating', 'comment', 'created_at']