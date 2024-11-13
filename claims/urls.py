from django.urls import path
from . import views

urlpatterns = [
    path('create/<str:serial_number>/', views.create_claim, name='create_claim'),
    path('view/<str:serial_number>/', views.view_claims, name='view_claims'),
]
