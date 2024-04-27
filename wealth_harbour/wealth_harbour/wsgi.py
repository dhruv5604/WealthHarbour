"""
WSGI config for wealth_harbour project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

    # import os

    # from django.core.wsgi import get_wsgi_application

    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wealth_harbour.settings')

    # application = get_wsgi_application()

import os
import sys

# Add the path to your Django project to the Python path
path = 'E:\SDP project\income-expense_home'  # Update this with the path to your Django project
if path not in sys.path:
    sys.path.append(path)

# Add the path to your virtual environment's site-packages directory
venv_path = '/home/wealthharbour/.virtualenvs/venv/lib/pythonX.X/site-packages'  # Update this with the path to your virtual environment
if venv_path not in sys.path:
    sys.path.append(venv_path)

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wealth_harbour.settings')

# Activate your virtual environment
activate_this = os.path.join(venv_path, 'activate_this.py')
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Load the Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
