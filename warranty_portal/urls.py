from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home, health_check

urlpatterns = [
    path('', home, name='home'), # home URLs
    path('admin/', admin.site.urls),
    path('products/', include('registrations.urls')),# registrations app URLs
    path('claims/', include('claims.urls')), # claims app URLs
    path('accounts/', include('accounts.urls')),  # accounts app URLs
    path('health/', health_check, name='health_check'),  # Health check endpoint
]

# Static and media file handling during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
