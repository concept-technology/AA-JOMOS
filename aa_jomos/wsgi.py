
import os

from django.core.wsgi import get_wsgi_application

from aa_jomos.settings import DEBUG

setting_module =   'aa_jomos.development' if DEBUG else 'aa_jomos.settings'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', setting_module)

application = get_wsgi_application()
