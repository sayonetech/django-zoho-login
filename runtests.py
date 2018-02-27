""" run tests for django-zoho-login
$ virtualenv ve
$ ./ve/bin/pip install Django
$ ./ve/bin/python runtests.py
"""


import django
from django.conf import settings
from django.core.management import call_command


def main():
    # Dynamically configure the Django settings with the minimum necessary to
    # get Django running tests
    settings.configure(
        MIDDLEWARE_CLASSES=(
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),

        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
        }],

        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'zoho_login',
        ),
        TEST_RUNNER = 'django.test.runner.DiscoverRunner',
        COVERAGE_EXCLUDES_FOLDERS = ['migrations'],
        ROOT_URLCONF = [],
        PROJECT_APPS = [
            'zoho_login',
        ],
	ZOHO_LOGIN_EMAIL_DOMAINS = ['example.com'],
        # Django replaces this, but it still wants it. *shrugs*
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
                'HOST': '',
                'PORT': '',
                'USER': '',
                'PASSWORD': '',
            }
        },
    )

    try:
        # required by Django 1.7 and later
        django.setup()
    except AttributeError:
        pass

    # Fire off the tests
    call_command('test')

if __name__ == '__main__':
    main()
