"""
Common Settings for all Environments
"""

from pathlib import Path

# region base

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent.parent

# endregion

# region development

DEBUG = True

# endregion

# region auth/security

SECRET_KEY = '4!ab1y4xi0wky+3cd*(#9_1v1jnce6)522ju&)z&0fh%1!8^3m'

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'pb_user.User'

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

# endregion

# region django

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third party apps
    'rest_framework',
    'corsheaders',

    # project apps
    'apps.core.apps.CoreConfig',
    'apps.auth.apps.AuthConfig',
    'apps.user.apps.UserConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'apps.auth.middlewares.fill_user_info',
    'apps.auth.middlewares.fill_permission_info',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # project middlewares
]

ROOT_URLCONF = 'base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'base.wsgi.application'

# endregion

# region django rest framework

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'utils.errors.custom_handler.exception_handler'
}

# endregion

# region database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mydb',
        'USER': 'postgresuser',
        'PASSWORD': 'postgrespass',
        'HOST': 'localhost',
        'PORT': 6432,
    }
}

# endregion

# region language

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# endregion

# region static/media

STATIC_URL = '/static/'

# endregion

# region logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple' if DEBUG else 'verbose',
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
    },
    'root': {
        'handlers': ['console'],
    },
}

# endregion

# region cors

CORS_ALLOW_ALL_ORIGINS = True

# endregion

# region other

APPEND_SLASH = True

# endregion

# region application

PAGE_SIZE = 20
OTP_CODE_LENGTH = 6
OTP_CODE_DURATION = {'minutes': 2}

AUTH_ACCESS_TOKEN_KEY = 'aklsdjfalkjsgh;adjkop32p9ry23-r9y2nfmna,.bzxcvh qpeyq hroqiq2gr'
AUTH_ACCESS_TOKEN_DURATION = {'days': 1}
AUTH_REFRESH_TOKEN_KEY = 'p23;k;lksl;jkasdofalskdasdhdfklhj23nkcsndclna923hjna'
AUTH_REFRESH_TOKEN_DURATION = {'days': 30}

# endregion
