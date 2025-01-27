import os
from pathlib import Path
import environ
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = Path(__file__).resolve().parent

env = environ.Env(DEBUG=(bool, False), EMAIL_USE_TLS=(bool, False), EMAIL_USE_SSL=(bool, False))
env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['www.localhost', 'localhost', '127.0.0.1', ]

INSTALLED_APPS = [
    # additional
    'ckeditor',  # RichTextField
    'mptt',  # Efficient technique for storing and retrieving hierarchical data in relational db (Categories)
    'admin_numeric_filter',
    'admin_auto_filters',  # Autocomplete filters
    'rangefilter',
    'modeltranslation',
    'rosetta',

    # default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # custom_apps
    'apps.common',
    'apps.carousel_banner',
    'apps.accents',
    'apps.products',
    'apps.text_pages',
    'apps.promotional_packages',
    'apps.contacts',
    'apps.users',
    'apps.orders',
    'apps.promo_codes',
    'apps.cards',
    'apps.carts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # CacheMiddleware if present must be before Locale
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # custom
    'apps.users.middlewares.CustomUserMiddleware',
]

CRON_CLASSES = [
    'apps.users.crons.OutdatedTokensCronJob',
]

ROOT_URLCONF = 'dundio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [PROJECT_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'dundio.context_processors.custom_processors',
            ],
        },
    },
]

WSGI_APPLICATION = 'dundio.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env('POSTGRES_NAME'),
        "USER": env('POSTGRES_USER'),
        "PASSWORD": env('POSTGRES_PASSWORD'),
        "HOST": env('POSTGRES_HOST'),
        "PORT": env('POSTGRES_PORT'),
    }
}


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

LANGUAGE_CODE = 'bg'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LANGUAGES = (  # ! restart the server to apply changes
    ('bg', _('Български')),
    ('en', _('Английски'))
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATICFILES_DIRS = [BASE_DIR / 'frontend']
STATIC_URL = '/static/'

LOGIN_URL = 'login'
INDEX_URL = 'index'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_USE_SSL = env('EMAIL_USE_SSL')  # booleans set with environ.Env()
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

CART_SESSION_ID = 'cart'
