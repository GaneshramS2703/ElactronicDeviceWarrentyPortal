from django.urls import path
from . import views

urlpatterns = [
    # Route to list all claims for the logged-in user
    path('list/', views.list_user_claims, name='list_user_claims'),
    # Route to create a new claim for a specific product identified by its serial number
    path('create/<str:serial_number>/', views.create_claim, name='create_claim'),
    # Route to view all claims related to a specific product identified by its serial number
    path('view/<str:serial_number>/', views.view_claims, name='view_claims'),
    # Route to delete a specific claim identified by its claim ID
    path('delete/<str:claim_id>/', views.delete_claim, name='delete_claim'),
]