"""
WSGI config for nextgen project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nextgen.settings')
os.environ['http_proxy'] = "http://127.0.0.1:8080"
application = get_wsgi_application()
