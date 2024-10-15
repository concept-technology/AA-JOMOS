
import os
from pathlib import Path
import environ
# Build paths inside the project like this: BASE_DIR / 'subdir'.
DEVELOPMENT = False

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
environ.Env.read_env(BASE_DIR / '.env')

ENVIRONMENT = 'production'

DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY')

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "phonenumber_field",
    'jazzmin',
    'allauth',
    'allauth.account',

    # Optional -- requires install using `django-allauth[socialaccount]`.
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'django.contrib.admin',
    'gunicorn',
    "corsheaders",
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
    'environ',
    'delivery',
    'paystack_api',
    # 'jet_django',
    'settings',
    # 'django_inline_actions'

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
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    # 'book_store.middleware.ignore_static_files.IgnoreStaticFilesMiddleware'
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
                'settings.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'aa_jomos.wsgi.application'


print("DJANGO_SETTINGS_MODULE:", os.environ.get("DJANGO_SETTINGS_MODULE"))

# https://docs.djangoproject.com/en/3.0/ref/settings/#allowed-hosts

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = [ALLOWED_HOSTS]
DEBUG = False

connection_string = os.environ.get('AZURE_POSTGRESQL_CONNECTIONSTRING')
parameters = {pair.split('-'):pair.slit('-')[1] for pair in connection_string.slit(' ')}


DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.postgresql', 
    'NAME':    parameters('dbname'),         
    'HOST': parameters('host'),                   
    'USER': parameters('user'),          
    'PASSWORD': parameters('password'),
    'PORT': parameters('DATABASE_PORT'),                       
}
}




PAYSTACK_PUBLIC_KEY = os.environ.get('PAYSTACK_PUBLIC_KEY')
PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY')

DEBUG_PROPAGATE_EXCEPTIONS = os.environ.get('DEBUG_PROPAGATE_EXCEPTIONS', default=False)
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = 465
# EMAIL_USE_TLS = True
EMAIL_USE_SSL = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
# Default email address to use for various automated correspondence
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = os.environ.get('EMAIL_HOST_USER')
ACCOUNT_EMAIL_REQUIRED = True


AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID') 
# AWS_ACCESS_KEY_ID = 'AKIAUBKFCNZRUXD6ZRVE'
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_SIGNATURE_NAME = os.environ.get('AWS_S3_SIGNATURE_NAME')
AWS_S3_REGION_NAME = 'eu-north-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL =  None
AWS_S3_VERIFY = True
AWS_QUERYSTRING_EXPIRE = 10
AWS_S3_CUSTOM_DOMAIN = 'd2nxnkp3c6n4f.cloudfront.net'
AWS_CLOUDFRONT_KEY_ID = os.environ.get('AWS_CLOUDFRONT_KEY_ID')
aws_cloudfront_key = os.environ.get('AWS_CLOUDFRONT_KEY', '')
AWS_CLOUDFRONT_KEY = aws_cloudfront_key.replace('\\n', '\n').encode('ascii').strip()




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
    # 'allauth.account.auth_backends.AuthenticationBackend',
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


LOGIN_REDIRECT_URL = '/'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'



ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False


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

# DEBUG_PROPAGATE_EXCEPTIONS = env('DEBUG_PROPAGATE_EXCEPTIONS', default=False)

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

