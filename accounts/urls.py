from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile_view'),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),  # Custom logout
]
