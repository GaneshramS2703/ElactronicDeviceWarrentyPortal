from pathlib import Path
import os

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^e49yxh0^)n447h1%x$86d!3!*v=mf^7o=atbkqdbf&ja2bhj+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allowed hosts for deployment
ALLOWED_HOSTS = [
    "3032a64f3919479dbd3e9de8324cfecd.vfs.cloud9.us-east-1.amazonaws.com"
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',  # Admin site
    'django.contrib.auth',  # Authentication
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom apps
    'accounts',
    'registrations',
    'claims',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'warranty_portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Add custom templates directory
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'warranty_portal.wsgi.application'

# Database Configuration
# No relational database is being used; DynamoDB will serve as the primary database.
DATABASES =  {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Disable migrations for Django models
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Password validation (Django’s auth system still requires this)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files configuration
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Media files configuration (optional, for S3 document uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# AWS Configuration
AWS_REGION = 'us-east-1'
DYNAMODB_TABLE_NAME = 'ProductWarrantyTable'  # DynamoDB table name
S3_BUCKET_NAME = 'warranty-documents-electronicdevices'  # S3 bucket name

# Logging (for debugging DynamoDB and S3 interactions)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'boto3': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'botocore': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

# Sessions and Authentication (Use DynamoDB for Sessions if needed)
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'  # Consider DynamoDB session integration later

CSRF_TRUSTED_ORIGINS = [
    'https://3032a64f3919479dbd3e9de8324cfecd.vfs.cloud9.us-east-1.amazonaws.com'
]


LOGIN_REDIRECT_URL = '/'  # Redirect to the home page after login

LOGIN_URL = '/accounts/login/'  # Redirect unauthenticated users to the login page
