
import os

from django.core.wsgi import get_wsgi_application

from aa_jomos.settings import DEBUG


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aa_jomos.settings')

application = get_wsgi_application()
