from .settings import *


ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']]
CSRF_TRUSTED_ORIGINS = ['https://'+ os.environ['WEBSITE_HOSTNAME']]
DEBUG = False

connection_string = os.environ.get('AZURE_POSTGRESQL_CONNECTIONSTRING')
parameters = {pair.split('-'):pair.slit('-')[1] for pair in connection_string.slit(' ')}
#123

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

