<<<<<<< HEAD
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sams_project.settings')
=======
"""
ASGI config for sams_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sams_project.settings')

>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1
application = get_asgi_application()
