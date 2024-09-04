
import os
from pathlib import Path
import environ
import dj_database_url

# AUTH_USER_MODEL = 'users.CustomUser'
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': 'django_debug.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# environ.Env.read_env(BASE_DIR / '.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-=13zeu+im=zl5$+k=)6@y65hkbn1458jlcf^cqtc%t4e$r2*2z'
SECRET_KEY =os.environ.get('SECRET_KEY', default='django-insecure-=13zeu+im=zl5$+k=)6@y65hkbn1458jlcf^cqtc%t4e$r2*2z')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', default=True)


INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'jazzmin',
    'django.contrib.admin',
    'gunicorn',
    'dj_database_url',
    "corsheaders",
    'allauth',
    'allauth.account',
    'allauth.socialaccount',   
    'allauth.socialaccount.providers.facebook',   
    'allauth.socialaccount.providers.google',   
    'PIL',
    'widget_tweaks',
    'rest_framework',
    'crispy_forms',
    "crispy_bootstrap4",
    'django_countries',
    'paystack',
    'dotenv',
    'paystackapi',
    'book_store',
    'star_ratings',
    'django.contrib.humanize',
    'requests',
    'xhtml2pdf',
    'environ'
    # 'jet_django',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    'book_store.middleware.ignore_static_files.IgnoreStaticFilesMiddleware'
]

ROOT_URLCONF = 'aa_jomos.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'aa_jomos.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'aa_jomos_database',
#         'USER': 'root',
#         'PASSWORD': 'Tamara1!',
#         'HOST': 'aa-jomos-database.c7y2yuoqejxn.eu-north-1.rds.amazonaws.com',
#         'PORT': '5432',
#         }
#     }

DATABASE_URL = env('DATABASE_URL')

DATABASES = {
    'default': dj_database_url.config(
        # Replace this value with your local database's connection string.
        default=DATABASE_URL,
        conn_max_age=600
    )
}
# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email'
        ],
        'AUTH_PARAMS': {'access_type': 'online'}
    }
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

JAZZMIN_SETTINGS = {
    "site_title": "A.A Jomos Ng ltd",
    "site_header": "A.A Jomos Ng ltd",
    "site_brand": "A.A Jomos Ng ltd",
}


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
USE_L10N = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = '/media/'


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]


  # Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = "storages.backends.s3.S3Storage"
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# https://docs.djangoproject.com/en/3.0/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# Application definition
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/profile/'  # Example redirect for authenticated users
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/login/'  # Example redirect for anonymous users

ACCOUNT_AUTHENTICATION_METHOD = "email"
LOGIN_REDIRECT_URL = 'store:index'
LOGOUT_REDIRECT_URL = 'store:index'
SIGNUP_REDIRECT_URL = 'store:index'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_HMAC = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True  # Auto-login after email confirmation
# ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1  # Example: 1 day until the confirmation link expires

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
# Default email address to use for various automated correspondence
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')


ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'


ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False


AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID') 
AWS_ACCESS_KEY_ID = 'AKIAUBKFCNZRUXD6ZRVE'
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_SIGNATURE_NAME = env('AWS_S3_SIGNATURE_NAME')
AWS_S3_REGION_NAME = 'eu-north-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL =  None
AWS_S3_VERIFY = True
AWS_QUERYSTRING_EXPIRE = 10
AWS_S3_CUSTOM_DOMAIN = 'd2nxnkp3c6n4f.cloudfront.net'
AWS_CLOUDFRONT_KEY_ID = env.str('AWS_CLOUDFRONT_KEY_ID').strip()
AWS_CLOUDFRONT_KEY = env.str('AWS_CLOUDFRONT_KEY', multiline=True).encode('ascii').strip()

CRISPY_TEMPLATE_PACK = 'bootstrap4'
CRISPY_TEMPLATE_PACK = 'bootstrap4'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 1
}

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True

DEBUG_PROPAGATE_EXCEPTIONS = os.environ.get('DEBUG_PROPAGATE_EXCEPTIONS', default=False)

# Custom settings
STAR_RATINGS_STAR_HEIGHT = 20
STAR_RATINGS_STAR_WIDTH = 20
STAR_RATINGS_RERATE = False
SITE_ID = 1

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email'
        ],
        'AUTH_PARAMS': {'access_type': 'online'}
    }
}

CART_SESSION_ID = 'cart'

INTERNAL_IPS = [
    "127.0.0.1",
]

ACCOUNT_FORMS = {
    'add_email': 'allauth.account.forms.AddEmailForm',
    'change_password': 'allauth.account.forms.ChangePasswordForm',
    'login': 'allauth.account.forms.LoginForm',
    'reset_password': 'allauth.account.forms.ResetPasswordForm',
    'reset_password_from_key': 'allauth.account.forms.ResetPasswordKeyForm',
    'set_password': 'allauth.account.forms.SetPasswordForm',
    'signup': 'allauth.account.forms.SignupForm',
    'user_token': 'allauth.account.forms.UserTokenForm',
}

PAYSTACK_PUBLIC_KEY = env('PAYSTACK_PUBLIC_KEY')
PAYSTACK_SECRET_KEY = env('PAYSTACK_SECRET_KEY')

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#     },
# }
