from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

SERVER_ADRESS = os.getenv("SERVER_ADRESS"
                         # , 'bf27-45-130-2-37.ngrok.io'
                          )
SECRET_KEY = os.getenv("SECRET_KEY", 'django-insecure-b5mww^d-9!5k+9i8%2s0vzyh54eqgr#k9810*(^w$vid0^d*t0')
TOKEN = os.getenv("TOKEN"
                  , '5420343912:AAHmj752TQOLi6JdKHYygJJpnqu0WtJBEdo'
                  )
DEBUG = os.getenv("DEBUG", "False")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")
DB_HOST = os.getenv("DB_HOST", "stage-db-26-08-22-backup-do-user-11581829-0.b.db.ondigitalocean.com")
DB_NAME = os.getenv("DB_NAME", "220822-stage")
DB_USER = os.getenv("DB_USER", "doadmin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "AVNS_0r_wo19DtRMwwCjS0KK")

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
    'partner_program',
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
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': 25060,
    },

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
    'MODE': 'WEBHOOK',
    'WEBHOOK_SITE': f'https://{SERVER_ADRESS}',
    'WEBHOOK_PREFIX': '/prefix',
    'BOTS': [
        {
            'TOKEN': TOKEN,
        },
    ],
}
