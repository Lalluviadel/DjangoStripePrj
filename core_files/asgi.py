"""
ASGI config for DjangoStripePrj project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_files.settings')

application = get_asgi_application()
