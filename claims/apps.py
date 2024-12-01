from django.apps import AppConfig

#Configuration class for the 'claims' application
class ClaimsConfig(AppConfig):
# Specifies the default primary key type for models in this app.
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'claims' #Application name
