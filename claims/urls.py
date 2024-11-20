from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.list_user_claims, name='list_user_claims'),
    path('create/<str:serial_number>/', views.create_claim, name='create_claim'),
    path('view/<str:serial_number>/', views.view_claims, name='view_claims'),
    path('delete/<str:claim_id>/', views.delete_claim, name='delete_claim'),
]