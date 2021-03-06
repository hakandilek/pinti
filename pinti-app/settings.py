# Initialize App Engine and import the default settings (DB backend, etc.).
# If you want to use a different backend you have to remove all occurences
# of "djangoappengine" from this file.
from djangoappengine.settings_base import *
import os

SECRET_KEY = 'cokgizli'

GLOBALTAGS = (
    'django.templatetags.i18n',
)

INSTALLED_APPS = (
    #registration should come before admin in order to override templates              
    'registration',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'djangotoolbox',
    'mediagenerator',
    'pinti',
    'minimar',
    
    # djangoappengine should come last, 
    #   so it can override a few manage.py commands
    'djangoappengine',
)

MIDDLEWARE_CLASSES = (
    # Media middleware has to come first
    'mediagenerator.middleware.MediaMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',    
)

TEMPLATE_CONTEXT_PROCESSORS = ( 
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.debug', 
    'django.core.context_processors.i18n',
    
)

# This test runner captures stdout and associates tracebacks with their
# corresponding output. Helps a lot with print-debugging.
TEST_RUNNER = 'djangotoolbox.test.CapturingTestSuiteRunner'

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)

ADMIN_MEDIA_PREFIX = '/media/admin/'
ROOT_URLCONF = 'urls'
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL    = '/accounts/login_error/'


# Activate django-dbindexer if available
try:
    import dbindexer
    DATABASES['native'] = DATABASES['default']
    DATABASES['default'] = {'ENGINE': 'dbindexer', 'TARGET': 'native'}
    INSTALLED_APPS += ('dbindexer',)
    DBINDEXER_SITECONF = 'dbindexes'
    MIDDLEWARE_CLASSES = ('dbindexer.middleware.DBIndexerMiddleware',) + \
                         MIDDLEWARE_CLASSES
except ImportError:
    pass

ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window; you may, of course, use a different value.
DEFAULT_FROM_EMAIL= 'no-reply@minimalabs.com'

#django-mediagenerator
MEDIA_DEV_MODE = DEBUG
DEV_MEDIA_URL = '/devmedia/'
PRODUCTION_MEDIA_URL = '/media/'
GLOBAL_MEDIA_DIRS = (os.path.join(os.path.dirname(__file__), 'static'),
                     os.path.join(os.path.dirname(__file__), 'django/contrib/admin/media'),)
MEDIA_BUNDLES = (
    ('main.css',
        'css/base.css',
        'css/forms.css',
        'css/ie.css',
        'css/jquery.fcbkcomplete.css',
    ),
    ('main.js',
        'js/jquery.js',
        'js/jquery.fcbkcomplete.js',
    ),
    ('draw.css',
        'css/jquery.svg.css',
        'css/draw_distribution.css',
    ),
    ('draw.js',
        'js/jquery.js',
        'js/jquery.svg.js',
        'js/jquery.drawinglibrary.js',
    ),
)


ugettext = lambda s: s

LANGUAGES = (
    ('tr', ugettext('Turkish')),
    ('en', ugettext('English')),
)
