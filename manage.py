#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """
    The entry point for running administrative tasks in the Django project.
    This function sets the default settings module and delegates the
    command-line arguments to Django's management utility.
    """
    # Set the default Django settings module for the 'warranty_portal' project
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'warranty_portal.settings')
    try:
        
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Raise an error if Django is not installed or the environment is misconfigured
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Execute the command-line arguments with Django's management utility
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
