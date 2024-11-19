from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile

@login_required
def profile_view(request):
    """Display and update the logged-in user's profile information."""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number', '').strip()
        address = request.POST.get('address', '').strip()
        
        if not phone_number:
            messages.error(request, 'Phone number is required.')
        else:
            profile.phone_number = phone_number
            profile.address = address
            profile.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile_view')

    return render(request, 'accounts/profile.html', {'profile': profile})


def register_user(request):
    """Handle user registration."""
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password1 = request.POST.get('password1').strip()
        password2 = request.POST.get('password2').strip()

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
        else:
            user = User.objects.create_user(username=username, password=password1)
            user.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')

    return render(request, 'accounts/register.html')


def login_user(request):
    """Handle user login."""
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profile_view')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')
