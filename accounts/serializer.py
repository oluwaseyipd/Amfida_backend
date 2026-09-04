from rest_framework import serializers
from .models import User, LandLordProfile, AgentProfile, OtpVerification

class LandlordProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandLordProfile
        fields = ['verification_status', 'id_document_url', 'property_proof_url', 'profile_avatar', 'verified_at']


class AgentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentProfile
        fields = ['verification_status', 'profile_avatar', 'verified_at']
    

class UserSerializer(serializers.ModelSerializer):

    landlord_profile = LandlordProfileSerializer(read_only=True)
    agent_profile = AgentProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'landlord_profile', 'agent_profile', 'is_active', 'is_staff', 'date_joined', 'last_login']

class OtpVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    phone_number = serializers.CharField(max_length=15, required=False, allow_blank=True)

    def validate(self, data):
        if not data.get('email') and not data.get('phone_number'):
            raise serializers.ValidationError("You must provide either an email or a phone number to receive an OTP.")
        return data

