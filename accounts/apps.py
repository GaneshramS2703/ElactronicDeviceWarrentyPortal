from django.apps import AppConfig

 # Configuration class for the 'accounts' application in Django.
class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'#application name

    def ready(self):
        # Import and register signals when the application is ready.
        # This ensures custom signal handlers (e.g., for user profile creation) are loaded.
        import accounts.signals  # Import signals to register them
