=====
django-zoho-login
=====

Django-zoho-login is simple wrapper to login in a django application using zoho username and password.

# Setup

1. Add `zoho_login` in the `INSTALLED_APPS`
2. Add ZOHO_LOGIN_EMAIL_DOMAINS eg: [google.com, sayonetech.com].
3. Add .'zoho_login.backends.ZohoApiBackend' in the AUTHENTICATION_BACKENDS settings.

.. code:: python
	AUTHENTICATION_BACKENDS = (
	    'django.contrib.auth.backends.ModelBackend',
	    'zoho_login.backends.ZohoApiBackend',
	)


