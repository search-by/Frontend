from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
SERVER_ADRESS = 'sbfbbeadmin.com'
SECRET_KEY = 'django-insecure-b5mww^d-9!5k+9i8%2s0vzyh54eqgr#k9810*(^w$vid0^d*t0'
TOKEN = '1950319109:AAGUgUsCQ-5fvHASYkQsweg5atGNw4QzXRM'
DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_telegrambot',
    'bot',
    'rest_framework',
    'users',
    'tasks',
    #'plategki',
    'partner_program',
    #'raports',
    "corsheaders",
    'rangefilter',
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

ROOT_URLCONF = 'fe_bot.urls'

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

WSGI_APPLICATION = 'fe_bot.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'TEST_FE_1',
        'USER': 'TEST_FE_ADMIN',
        'PASSWORD': 'AVNS_u-hAhyKg7a6Si4Pbi8Z',
        'HOST': 'db-1-do-user-11581829-0.b.db.ondigitalocean.com',
        'PORT': 25060,
    },
    #'prod': {
    #    'ENGINE': 'django.db.backends.postgresql',
    #    'NAME': 'defaultdb',
    #    'USER': 'doadmin',
    #    'PASSWORD': 'AVNS_0r_wo19DtRMwwCjS0KK',
    #    'HOST': 'db-1-do-user-11581829-0.b.db.ondigitalocean.com',
    #    'PORT': 25060,
    #}
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DJANGO_TELEGRAMBOT = {
    'MODE' : 'WEBHOOK',
    'WEBHOOK_SITE' : f'https://{SERVER_ADRESS}',
    'WEBHOOK_PREFIX' : '/prefix',
    #WEBHOOK_CERTIFICATE' : '/etc/ssl/certs/nginx-selfsigned.crt',
    #'STRICT_INIT': True,
    'BOTS' : [
        {
            'TOKEN': TOKEN,
        },
    ],
}
