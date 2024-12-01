from pathlib import Path
import os

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^e49yxh0^)n447h1%x$86d!3!*v=mf^7o=atbkqdbf&ja2bhj+'

DEBUG = False  # Set to False for production

# Allowed hosts for deployment
ALLOWED_HOSTS = [
    "127.0.0.1",
    "3032a64f3919479dbd3e9de8324cfecd.vfs.cloud9.us-east-1.amazonaws.com",
    "warrantyandproductregistration-env.eba-bmrq3mke.us-east-1.elasticbeanstalk.com", #domain name
    "localhost",
    ".us-east-1.elb.amazonaws.com", # Elastic Load Balancer in us-east-1
    "172.31.83.118" #local Ip
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
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Default SQLite database for development
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


MIGRATION_MODULES = {
    # Keep default migrations for core Django apps
    'admin': None,
    'auth': None,
    'contenttypes': None,
    'sessions': None,
    'messages': None,
    
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Media files configuration (optional, for S3 document uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# AWS Configuration
AWS_REGION = 'us-east-1'
DYNAMODB_TABLE_NAME = 'ProductWarrantyTable'  # DynamoDB table name
S3_BUCKET_NAME = 'warranty-documents-electronicdevices'  # S3 bucket name

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {'handlers': ['console'], 'level': 'INFO'},
        'boto3': {'handlers': ['console'], 'level': 'INFO'},
        'botocore': {'handlers': ['console'], 'level': 'INFO'},
    },
}

# CSRF and Authentication
CSRF_TRUSTED_ORIGINS = [
    'https://3032a64f3919479dbd3e9de8324cfecd.vfs.cloud9.us-east-1.amazonaws.com',
]

LOGIN_REDIRECT_URL = '/'  # Redirect to home page after login
LOGIN_URL = '/accounts/login/'  # Redirect unauthenticated users to login page

# Sessions (optional: Use Django’s default DB-backed session engine)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Collectstatic configuration
COLLECTSTATIC_STRICT = True
