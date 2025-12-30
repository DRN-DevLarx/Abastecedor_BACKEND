import os
from decouple import config
from pathlib import Path
from datetime import timedelta
import pymysql
pymysql.install_as_MySQLdb()

# from dotenv import load_dotenv
# load_dotenv(BASE_DIR / '.env')

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)



ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    "api",
    "corsheaders",
]

# REST_FRAMEWORK = {
#     "DEFAULT_AUTHENTICATION_CLASSES": [
#         "rest_framework_simplejwt.authentication.JWTAuthentication",
#     ],
#     "DEFAULT_PERMISSION_CLASSES": [
#         "rest_framework.permissions.IsAuthenticated",
#     ],
# }

# DEFAULT_AUTHENTICATION_CLASSES = [
#     "ruta.a.CookieJWTAuthentication",
# ]


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Temporalmente para probar
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=20),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_COOKIE': 'jwt_token',    #Nombre de la cookie que almacenará el JWT.
    'AUTH_COOKIE_SECURE': False,    #Si está en False, la cookie se enviará incluso en conexiones no seguras (HTTP). Debería estar en True en producción.
    'AUTH_COOKIE_HTTP_ONLY': True,  #Si está en True, impide que el cliente acceda a la cookie mediante JavaScript (mayor seguridad contra ataques XSS).
    'AUTH_COOKIE_SAMESITE': 'Lax',  #Se establece en 'Lax', lo que significa que la cookie solo se enviará en solicitudes de primer nivel o navegación. Previene ataques CSRF sin bloquear completamente los enlaces de terceros.z
}

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_NAME = "sessionid"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]


ROOT_URLCONF = 'abastecedor.urls'

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

WSGI_APPLICATION = 'abastecedor.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'abastecedor',
#         'USER': 'root',
#         'PASSWORD':'',
#         'HOST': '127.0.0.1',
#         'PORT':'3306'
#     }
# }

from decouple import config

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='3306'),
        'OPTIONS': {
            'ssl_mode': config('DB_SSL_MODE', default='REQUIRED'),
            'charset': 'utf8mb4',
            'connect_timeout': 10,
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_CREDENTIALS = True   #permite que las solicitudes cross-origin incluyan credenciales como cookies, autenticaciones HTTP o encabezados de autorización.

CORS_ALLOWED_ORIGINS=[
    "http://localhost:5173",
    # "https://apis.gometa.org",
    
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
]


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'darienaguilar3000@gmail.com'
EMAIL_HOST_PASSWORD = 'depztcyrvjtvmrms'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
