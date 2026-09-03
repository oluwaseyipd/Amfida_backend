from django.db import models



class LandLord(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=255)
    verification_status = models.CharField(max_length=50, default='unverified')
    id_document_url = models.URLField(blank=True, null=True)
    property_proof_url = models.URLField(blank=True, null=True)
    profile_avatar = models.ImageField(upload_to='landlord_profiles/avatars/', blank=True, null=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Agent(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=255)
    verification_status = models.CharField(max_length=50, default='unverified')
    aggency_approval=models.CharField(max_length=50, default='unapproved')
    profile_avatar = models.ImageField(upload_to='agent_profiles/avatars/', blank=True, null=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class OtpVerification(models.Model):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"OTP for {self.user.email} - Verified: {self.is_verified}"