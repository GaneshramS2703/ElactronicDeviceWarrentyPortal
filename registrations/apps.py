from django.apps import AppConfig

#Configuration class for the 'registrations' app.
class RegistrationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField' # Sets the default field type for auto-generated primary keys
    name = 'registrations' # Specifies the name of the app
