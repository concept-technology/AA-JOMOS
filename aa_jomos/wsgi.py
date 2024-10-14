"""
WSGI config for aa_jomos project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

settings_module = 'aa_jomos.deployment' if 'WEBSITE_HOSTNAME' in os.environ else 'aajomos.settings'


os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aa_jomos.settings')

application = get_wsgi_application()
