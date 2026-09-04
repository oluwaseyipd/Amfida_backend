from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models



# Create a custom user manager to enable the terminal to create superusers with email instead of username
class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# Create a custom user model by extending AbstractUser
class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = None # use email for login instead of username
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email' # force login with email instead of username
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']


    def __str__(self):
            return f"{self.first_name} {self.last_name}"


# Create a LandlordProfile model to store additional information for landlords
class LandLordProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='landlord_profile')
    verification_status = models.CharField(max_length=50, default='unverified')
    id_document_url = models.URLField(blank=True, null=True)
    property_proof_url = models.URLField(blank=True, null=True)
    profile_avatar = models.ImageField(upload_to='landlord_profiles/avatars/', blank=True, null=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    
    
    def __str__(self):
        return f"Landlord - {self.user.first_name} {self.user.last_name}"


# Create an AgentProfile model to store additional information for agents
class AgentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent_profile')
    verification_status = models.CharField(max_length=50, default='unverified')
    aggency_approval=models.CharField(max_length=50, default='unapproved')
    profile_avatar = models.ImageField(upload_to='agent_profiles/avatars/', blank=True, null=True)
    verified_at = models.DateTimeField(blank=True, null=True)

    
    def __str__(self):
        return f"Agent - {self.user.first_name} {self.user.last_name}"


# Create an OtpVerification model to store OTP codes for email and phone number verification
class OtpVerification(models.Model):
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"OTP for {self.email} - Verified: {self.is_verified}"