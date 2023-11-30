"""WSGI config for DjangoStripePrj project."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_files.settings')

application = get_wsgi_application()
