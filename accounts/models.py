from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class UserProfile(models.Model):
    # Link the UserProfile to a specific User, ensuring a one-to-one relationship.
    # The cascade delete ensures the UserProfile is deleted if the User is removed.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Store the user's phone number with validation for proper formatting.
    # Allows optional input (blank=True, null=True).
    phone_number = models.CharField(
        max_length=15,  # Restrict phone number length to a maximum of 15 characters.
        blank=True,  # Allow phone_number to be optional in forms.
        null=True,  # Allow phone_number to be empty in the database.
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',  # Enforce a pattern for valid international phone numbers.
            message="Enter a valid phone number."  # Error message for invalid phone numbers.
        )]
    )

    # Field for storing the user's address, optional input allowed.
    address = models.TextField(blank=True, null=True)

    # Customize metadata for the model, including the singular and plural names.
    class Meta:
        verbose_name = "User Profile"  # Singular name used in admin and forms.
        verbose_name_plural = "User Profiles"  # Plural name used in admin and forms.

    # String representation of the UserProfile object for debugging and admin displays.
    def __str__(self):
        return f"{self.user.username}'s Profile"

    # Method to fetch the user's full address, including their phone number if available.
    def get_full_address(self):
        return f"{self.address} ({self.phone_number})" if self.phone_number else self.address
