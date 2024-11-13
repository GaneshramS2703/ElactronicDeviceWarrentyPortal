# accounts/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def profile_view(request):
    """Display the logged-in user's profile information."""
    # Get the profile associated with the current logged-in user
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': profile})
