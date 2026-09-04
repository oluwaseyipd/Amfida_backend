from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, LandLordProfile, AgentProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        
        # If the user is a staff member or superuser, we don't want to create a profile for them
        if instance.is_staff or instance.is_superuser:
            return

        is_agent = getattr(instance, 'is_agent_signup', False)
        
        if is_agent:
            AgentProfile.objects.create(user=instance)
        else:
            LandLordProfile.objects.create(user=instance)
