"""
WSGI config for lemon project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import sys


# Add the site-packages of the chosen virtualenv to work
# site.addsitedir('~/.virtualenvs/myprojectenv/local/lib# /phython2.7/site-packages')


path = "/var/www/MediaServices/media_bliss_api/bliss"
# path = "/home/centos/MediaServices/media_bliss_api/bliss"
sys.path.append(path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

