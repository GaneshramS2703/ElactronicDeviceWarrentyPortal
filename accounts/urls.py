from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile_view'),  # View to display and update the user's profile.
    path('register/', views.register_user, name='register_user'),  # View for user registration.
    path('login/', views.login_user, name='login'),  # View for user login.
    path('logout/', views.logout_user, name='logout'),  # Custom logout view to handle user logout.
]