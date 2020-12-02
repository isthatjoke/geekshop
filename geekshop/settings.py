#Django settings for geekshop project.

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = BASE_DIR + '/geekshop/json/'


# SECURITY WARNING: keep the secret key used in production secret!
with open(JSON_PATH + 'secret_key.json') as secret_key:
    SECRET_KEY = json.load(secret_key)
SECRET_KEY = SECRET_KEY['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = False

# if DEBUG:
#    def show_toolbar(request):
#        return True
#
# DEBUG_TOOLBAR_CONFIG = {
#        'SHOW_TOOLBAR_CALLBACK': show_toolbar,
#    }
#
# DEBUG_TOOLBAR_PANELS = [
#     'debug_toolbar.panels.versions.VersionsPanel',
#     'debug_toolbar.panels.timer.TimerPanel',
#     'debug_toolbar.panels.settings.SettingsPanel',
#     'debug_toolbar.panels.headers.HeadersPanel',
#     'debug_toolbar.panels.request.RequestPanel',
#     'debug_toolbar.panels.sql.SQLPanel',
#     'debug_toolbar.panels.templates.TemplatesPanel',
#     'debug_toolbar.panels.staticfiles.StaticFilesPanel',
#     'debug_toolbar.panels.cache.CachePanel',
#     'debug_toolbar.panels.signals.SignalsPanel',
#     'debug_toolbar.panels.logging.LoggingPanel',
#     'debug_toolbar.panels.redirects.RedirectsPanel',
#     'debug_toolbar.panels.profiling.ProfilingPanel',
#     'template_profiler_panel.panels.template.TemplateProfilerPanel',
#     ]


ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mainapp',
    'authapp',
    'shopping_cartapp',
    'adminapp',
    'social_django',
    'ordersapp',
    'searchapp',
    # 'debug_toolbar',
    # 'template_profiler_panel',
    # 'django_extensions',
    'rest_framework',
    'apiapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'geekshop.urls'

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
                'mainapp.context_processors.shopping_cart',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'geekshop.wsgi.application'


# Database

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'geekshop',
        'USER': 'django',
        'PASSWORD': 'geekbrains',
        'HOST': 'localhost',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
AUTH_USER_MODEL = 'authapp.ShopUser'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.vk.VKOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.github.GithubOAuth2',
)


#VK
with open(JSON_PATH + 'vk.json') as vk:
    VK = json.load(vk)

SOCIAL_AUTH_VK_OAUTH2_KEY = VK['SOCIAL_AUTH_VK_OAUTH2_KEY']
SOCIAL_AUTH_VK_OAUTH2_SECRET = VK['SOCIAL_AUTH_VK_OAUTH2_SECRET']
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_VK_OAUTH2_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']

#GOOGLE
with open(JSON_PATH + 'google.json') as google:
    GOOGLE = json.load(google)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = GOOGLE['SOCIAL_AUTH_GOOGLE_OAUTH2_KEY']
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = GOOGLE['SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET']
SOCIAL_AUTH_GOOGLE_OAUTH2_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/user.birthday.read',
    'https://www.googleapis.com/auth/user.gender.read',
]

#GITHUB
with open(JSON_PATH + 'github.json') as github:
    GITHUB = json.load(github)

SOCIAL_AUTH_GITHUB_KEY = GITHUB['SOCIAL_AUTH_GITHUB_KEY']
SOCIAL_AUTH_GITHUB_SECRET = GITHUB['SOCIAL_AUTH_GITHUB_SECRET']
SOCIAL_AUTH_GITHUB_SCOPE = ['user:email']

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.create_user',
    'authapp.pipeline.save_user_profile_vk',
    'authapp.pipeline.save_user_profile_google',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',

)

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-en'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = False

USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
LOGIN_URL = '/auth/login/'
LOGIN_ERROR_URL = '/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


# email

with open(JSON_PATH + 'gmail_email.json') as gmail:
    GMAIL = json.load(gmail)


DOMAIN_NAME = 'djangopj.ru'
SERVER_NAME = 'djangopj.ru'
# DOMAIN_NAME = 'http://localhost:8000'
# SERVER_NAME = 'http://localhost:8000'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = GMAIL['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = GMAIL['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = True
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# EMAIL_USE_SSL = False
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#yandex 'wypksowgdnhotxio'
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = '25'
# EMAIL_HOST_USER = 'django@geekshop.local'
# EMAIL_HOST_PASSWORD = 'geekshop'
# EMAIL_USE_SSL = False
# EMAIL_HOST_USER, EMAIL_HOST_PASSWORD = None, None
# EMAIL_FILE_PATH = 'tmp/email-messages/'

#cache

if os.name == 'posix':
    CACHE_MIDDLEWARE_ALIAS = 'default'
    CACHE_MIDDLEWARE_SECONDS = 120
    CACHE_MIDDLEWARE_KEY_PREFIX = 'geekshop'

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211'
        }
    }

LOW_CACHE = True
