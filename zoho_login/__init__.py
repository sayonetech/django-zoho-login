import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

if 'zoho_login' in settings.INSTALLED_APPS:
    # Confirm ZOHO_LOGIN_EMAIL_DOMAINS setting has been specified.
    # This variable will identify our users/ company members are login to system
    try:
        settings.ZOHO_LOGIN_EMAIL_DOMAINS
    except AttributeError:
        raise ImproperlyConfigured("django-zoho-login requires \
                ZOHO_LOGIN_EMAIL_DOMAINS setting. It will be the list of email domains \
		that we need to support for zoho login.")
