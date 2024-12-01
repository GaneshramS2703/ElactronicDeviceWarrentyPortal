from django.urls import path
from . import views

urlpatterns = [
    # URL for creating a new product with warranty details and document upload
    path('create/', views.create_product, name='create_product'),
    # URL for viewing the details of a specific product using its serial number
    path('view/<str:serial_number>/', views.view_product, name='view_product'),
    # URL for directly deleting a product (no confirmation page)
    path('delete/<str:serial_number>/', views.delete_product, name='delete_product'),
     # URL for displaying a confirmation page before deleting a product
    path('delete/confirm/<str:serial_number>/', views.delete_product_confirmation, name='delete_product_confirmation'),
    # URL for listing all products registered by the logged-in user
    path('list/', views.list_products, name='list_products'),
]
