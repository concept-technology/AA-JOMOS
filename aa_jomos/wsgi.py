
import os

from django.core.wsgi import get_wsgi_application

setting_module = 'aa_jomos.deployment' if 'WEBSITE_HOSTNAME' in os.environ else 'aa_jomos.settings'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', setting_module)

application = get_wsgi_application()
