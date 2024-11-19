from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'serial_number', 'purchase_date', 'warranty_period', 'user')
    search_fields = ('product_name', 'serial_number', 'user__username')
    list_filter = ('purchase_date', 'warranty_period')
