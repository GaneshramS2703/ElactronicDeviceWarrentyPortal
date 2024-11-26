"""
WSGI config for warranty_portal project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'warranty_portal.settings')

# Original application
django_application = get_wsgi_application()

# Wrapper application to handle missing CONTENT_LENGTH
def application(environ, start_response):
    # Ensure CONTENT_LENGTH is always set to avoid KeyError
    environ['CONTENT_LENGTH'] = environ.get('CONTENT_LENGTH', '0')
    return django_application(environ, start_response)
