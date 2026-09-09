from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, LandLordProfile, AgentProfile, OtpVerification


class LandlordProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandLordProfile
        fields = ['verification_status', 'id_document_url', 'property_proof_url', 'profile_avatar', 'verified_at']


class AgentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentProfile
        fields = ['verification_status', 'agency_approval', 'profile_avatar', 'verified_at']


class UserSerializer(serializers.ModelSerializer):
    landlord_profile = LandlordProfileSerializer(read_only=True)
    agent_profile = AgentProfileSerializer(read_only=True)
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone_number',
            'role', 'landlord_profile', 'agent_profile',
            'is_active', 'is_staff', 'date_joined', 'last_login'
        ]

    def get_role(self, obj):
        if hasattr(obj, 'agent_profile'):
            return 'agent'
        elif hasattr(obj, 'landlord_profile'):
            return 'landlord'
        return 'user'


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(choices=['landlord', 'agent'], default='landlord', write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'password', 'role']

    def validate_password(self, value):
        validate_password(value, self.instance)
        return value

    def create(self, validated_data):
        role = validated_data.pop('role', 'landlord')
        user = User.objects.create_user(**validated_data)
        if role == 'agent':
            AgentProfile.objects.get_or_create(user=user)
        else:
            LandLordProfile.objects.get_or_create(user=user)
        return user


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    profile_avatar = serializers.ImageField(required=False, allow_null=True)
    id_document_url = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    property_proof_url = serializers.URLField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'profile_avatar', 'id_document_url', 'property_proof_url']

    def update(self, instance, validated_data):
        avatar = validated_data.pop('profile_avatar', None)
        id_doc = validated_data.pop('id_document_url', None)
        prop_proof = validated_data.pop('property_proof_url', None)

        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()

        # Update profile fields if applicable
        if hasattr(instance, 'landlord_profile'):
            profile = instance.landlord_profile
            if avatar is not None:
                profile.profile_avatar = avatar
            if id_doc is not None:
                profile.id_document_url = id_doc
            if prop_proof is not None:
                profile.property_proof_url = prop_proof
            profile.save()
        elif hasattr(instance, 'agent_profile'):
            profile = instance.agent_profile
            if avatar is not None:
                profile.profile_avatar = avatar
            profile.save()

        return instance


class OtpVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    phone_number = serializers.CharField(max_length=15, required=False, allow_blank=True)

    def validate(self, data):
        if not data.get('email') and not data.get('phone_number'):
            raise serializers.ValidationError("You must provide either an email or a phone number to receive an OTP.")
        return data
