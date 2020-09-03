
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'camunda.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'BaseConfiguration')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
