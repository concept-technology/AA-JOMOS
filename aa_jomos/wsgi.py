
import os

from django.core.wsgi import get_wsgi_application

production = 1
setting_module = 'aa_jomos.settings' if production else 'aa_jomos.deployment'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', setting_module)

application = get_wsgi_application()
