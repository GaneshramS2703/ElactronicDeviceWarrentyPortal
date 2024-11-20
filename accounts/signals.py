import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile whenever a new User is created."""
    if created:
        UserProfile.objects.create(user=instance)
        logger.info(f"UserProfile created for user: {instance.username}")

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the UserProfile whenever the User is saved."""
    try:
        instance.userprofile.save()
        logger.info(f"UserProfile saved for user: {instance.username}")
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)
        logger.warning(f"UserProfile was missing for user: {instance.username}. Created automatically.")
