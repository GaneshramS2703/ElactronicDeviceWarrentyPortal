from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_product, name='create_product'),
    path('view/<str:serial_number>/', views.view_product, name='view_product'),
    path('delete/<str:serial_number>/', views.delete_product, name='delete_product'),
    path('delete/confirm/<str:serial_number>/', views.delete_product_confirmation, name='delete_product_confirmation'),
    path('list/', views.list_products, name='list_products'),
]
