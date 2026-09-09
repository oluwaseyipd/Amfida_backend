from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, LandLordProfile, AgentProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Fallback profile creation signal if user is created directly outside the registration serializer.
    """
    if created:
        if instance.is_staff or instance.is_superuser:
            return

        has_profile = (
            hasattr(instance, 'landlord_profile')
            or hasattr(instance, 'agent_profile')
            or LandLordProfile.objects.filter(user=instance).exists()
            or AgentProfile.objects.filter(user=instance).exists()
        )

        if not has_profile:
            is_agent = getattr(instance, 'is_agent_signup', False)
            if is_agent:
                AgentProfile.objects.get_or_create(user=instance)
            else:
                LandLordProfile.objects.get_or_create(user=instance)
