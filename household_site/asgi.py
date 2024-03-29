"""
ASGI config for household_site project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import sys
sys.path.insert(0, "/home/harizcor/app/household/household_site")

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'household_site.settings')

application = get_asgi_application()
