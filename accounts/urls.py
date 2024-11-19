from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile_view'),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login'),
]
