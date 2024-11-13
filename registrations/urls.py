from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_product, name='create_product'),
    path('<str:serial_number>/', views.view_product, name='view_product'),
    path('<str:serial_number>/delete/', views.delete_product, name='delete_product'),
]
