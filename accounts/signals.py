import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

logger = logging.getLogger(__name__)

#Create a UserProfile whenever a new User is created.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created: # Check if the User instance was just created.
        UserProfile.objects.create(user=instance)  # Create a corresponding UserProfile.
        logger.info(f"UserProfile created for user: {instance.username}") # Log the creation event.
        
#Save the UserProfile whenever the User is saved.
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save() # Save the existing UserProfile linked to the User.
        logger.info(f"UserProfile saved for user: {instance.username}") # Log the save event.
    except UserProfile.DoesNotExist:  # Handle cases where the UserProfile does not exist.
        UserProfile.objects.create(user=instance) # Create a new UserProfile if missing.
        logger.warning(f"UserProfile was missing for user: {instance.username}. Created automatically.") # Log a warning
