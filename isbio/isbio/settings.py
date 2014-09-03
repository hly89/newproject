# Django settings for isbio project.
from configurations import Settings
import logging
import os
gettext = lambda s: s
PROJECT_PATH = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]


class BreezeSettings(Settings):
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG

    logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(funcName)s %(levelname)-8s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='/tmp/BREEZE.log', filemode='w')

    ADMINS = (
        # ('Dmitrii Bychkov', 'piter.dmitry@gmail.com'),
    )

    MANAGERS = ADMINS

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'biodb',  # Or path to database file if using sqlite3.
            'USER': 'root',  # Not used with sqlite3.
            'PASSWORD': '',  # Not used with sqlite3.
            'HOST': '',  # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '3306',  # Set to empty string for default. Not used with sqlite3.
            'OPTIONS': { "init_command": "SET foreign_key_checks = 0;", },
        }
    }

    # Local time zone for this installation. Choices can be found here:
    # http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
    # although not all choices may be available on all operating systems.
    # In a Windows environment this must be set to your system time zone.
    TIME_ZONE = 'Europe/Helsinki'

    # Language code for this installation. All choices can be found here:
    # http://www.i18nguy.com/unicode/language-identifiers.html
    LANGUAGE_CODE = 'en-us'
    
    LANGUAGES = (
        ('en-us', gettext('English')),
    )

    SITE_ID = 1

    # If you set this to False, Django will make some optimizations so as not
    # to load the internationalization machinery.
    USE_I18N = True

    # If you set this to False, Django will not format dates, numbers and
    # calendars according to the current locale.
    USE_L10N = True

    # If you set this to False, Django will not use timezone-aware datetimes.
    USE_TZ = True

    # !CUSTOM!
    # Tempory folder for the application
    TEMP_FOLDER = '/Users/liye/Documents/breeze/tmp/'
    # Path to R installation
    R_ENGINE_PATH = 'R '

    # Absolute filesystem path to the directory that will hold user-uploaded files.
    # Example: "/home/media/media.lawrence.com/media/"
    MEDIA_ROOT = '/Users/liye/Documents/breeze/db/'
    RORA_LIB = '/Users/liye/Documents/breeze/roralib/'

    # URL that handles the media served from MEDIA_ROOT. Make sure to use a
    # trailing slash.
    # Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
    MEDIA_URL = '/media/'

    # Absolute path to the directory static files should be collected to.
    # Don't put anything in this directory yourself; store your static files
    # in apps' "static/" subdirectories and in STATICFILES_DIRS.
    # Example: "/home/media/media.lawrence.com/static/"
    STATIC_ROOT = ''

    # URL prefix for static files.
    # Example: "http://media.lawrence.com/static/"
    STATIC_URL = '/static/'

    # Additional locations of static files
    STATICFILES_DIRS = (
        "/Users/liye/Documents/breeze/isbio-master/isbio/breeze/static",
        # Put strings here, like "/home/html/static" or "C:/www/django/static".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
    )

    # List of finder classes that know how to find static files in
    # various locations.
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'django.contrib.staticfiles.finders.DefaultStorageFinder',
    )

    # Make this unique, and don't share it with anybody.
    SECRET_KEY = 'ta(zaxdj#)wxg(g+7%f)^e6fu+l#0$y4@81t2g9jo%!i(82ue_'

    # List of callables that know how to import templates from various sources.
    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
    )

    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.doc.XViewMiddleware',
        # Uncomment the next line for simple clickjacking protection:
        # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'django_cas.backends.CASBackend',
    )

    CAS_SERVER_URL = 'https://192.168.0.218:8443/cas/'
    CAS_REDIRECT_URL = '/home/'

    ROOT_URLCONF = 'isbio.urls'

    # Python dotted path to the WSGI application used by Django's runserver.
    WSGI_APPLICATION = 'isbio.wsgi.application'

    TEMPLATE_DIRS = (
        '/Users/liye/Documents/breeze/isbio-master/isbio/breeze/templates',
        # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
    )
    MS_TEMPLATES_DIR = {
        '/Users/liye/Documents/breeze/isbio-master/isbio/breeze/templates',
    }
    # provide our profile model
    AUTH_PROFILE_MODULE = 'breeze.UserProfile'

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'bootstrap_toolkit',
        'breeze',
        'south',
        'gunicorn',
        'djangocms_admin_style',  # for the admin skin. You **must** add 'djangocms_admin_style' in the list **before** 'django.contrib.admin'.
        # Uncomment the next line to enable the admin:
        'django.contrib.admin',
        'cms', # django CMS itself
        'mptt',
        'menus',
        'shop', # the django shop app
        #'shop.addressmodel', # the default address and country model
        'sekizai', # for javascript and css management
        # Uncomment the next line to enable admin documentation:
        # 'django.contrib.admindocs',
    )
    
    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.doc.XViewMiddleware',
        'django.middleware.common.CommonMiddleware',
        'cms.middleware.user.CurrentUserMiddleware',
        'cms.middleware.page.CurrentPageMiddleware',
        'cms.middleware.toolbar.ToolbarMiddleware',
        'cms.middleware.language.LanguageCookieMiddleware',
    )

    # A sample logging configuration. The only tangible logging
    # performed by this configuration is to send an email to
    # the site admins on every HTTP 500 error when DEBUG=False.
    # See http://docs.djangoproject.com/en/dev/topics/logging for
    # more details on how to customize your logging configuration.
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            }
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
        }
    }

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'breeze.context.user_context',
        'django.contrib.messages.context_processors.messages',
        'django.core.context_processors.i18n',
        'sekizai.context_processors.sekizai',
        'django.core.context_processors.request',
    )

class DevSettings(BreezeSettings):
    DEBUG = True

    os.environ['LD_LIBRARY_PATH'] = '/opt/gridengine/lib/UNSUPPORTED-lx3.2.0-40-generic-amd64'
    os.environ['SGE_ROOT'] = '/opt/gridengine'
    os.environ['SGE_QMASTER_PORT'] = '536'
    os.environ['SGE_EXECD_PORT'] = '537'
    os.environ['SGE_ARCH'] = 'UNSUPPORTED-lx3.2.0-40-generic-amd64'
    os.environ['SGE_CELL'] = 'default'
    os.environ['DRMAA_LIBRARY_PATH'] = '/opt/gridengine/lib/lx26-amd64/libdrmaa.so'
    os.environ['MAIL'] = '/var/mail/dbychkov'


    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'breezedb',  # Or path to database file if using sqlite3.
            'USER': 'root',  # Not used with sqlite3.
            'PASSWORD': '',  # Not used with sqlite3.
            'HOST': '',  # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '3306',  # Set to empty string for default. Not used with sqlite3.
        }
    }

    R_ENGINE_PATH = '/Library/Frameworks/R.framework/Resources/bin/exec/R'
    TEMP_FOLDER = '/Users/liye/Documents/breeze/tmp/'
    MEDIA_ROOT = '/Users/liye/Documents/breeze/db/'  # '/homes/dbychkov/dev/isbio/db/'
    RORA_LIB = '/Users/liye/Documents/breeze/roralib/'

    MEDIA_URL = '/media/'

    STATIC_ROOT = '/Users/liye/Documents/breeze/isbio-master/isbio/breeze/static/'
    STATIC_URL = '/static/'

    # Additional locations of static files
    STATICFILES_DIRS = (
        "",
    )
