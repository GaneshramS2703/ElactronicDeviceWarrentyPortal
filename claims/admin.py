from django.contrib import admin
from .models import Claim

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('product', 'status', 'claim_date', 'description')
    search_fields = ('product__serial_number', 'status')
    list_filter = ('status', 'claim_date')
