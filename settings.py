# Base settings
import os, sys

PROJECT_ROOT                        = os.path.dirname(__file__)

# Environment
# ===========
SITE_ID                             = 1
DEBUG                               = True
TEMPLATE_DEBUG                      = DEBUG
TESTING = sys.argv[1:2] == ['test']

# Paths
# ======
sys.path.insert(0, os.path.join(PROJECT_ROOT, "lib"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "apps"))

# static media
STATIC_ROOT                         = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL                          = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static_app'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)
STATICFILES_STORAGE = \
    'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

# user uploaded files
MEDIA_ROOT                          = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL                           = '/media/'
ADMIN_MEDIA_PREFIX                  = '/static/admin/'
CKEDITOR_UPLOAD_PATH                = MEDIA_ROOT + '/articles/attach/upload/'
CKEDITOR_RESTRICT_BY_USER           = True
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
        'height': 300,
        'width': 600,
    },
}


# Other django settings
# =====================
INTERNAL_IPS                        = ('127.0.0.1',)
LANGUAGE_CODE                       = 'en-gb'
SECRET_KEY                          = 't_)g0#fic+!kbay3#_#jotx-ryh$t1c$q!h_+@!hm1mvy_83#n'
TIME_ZONE                           = 'UTC'  # 'Europe/London'
USE_TZ                              = True
USE_ETAGS                           = False
DEFAULT_CHARSET                     = 'utf-8'
USE_I18N                            = False
USE_L10N                            = False
PREPEND_WWW                         = False
ROOT_URLCONF                        = 'urls'
AUTH_PROFILE_MODULE                 = 'accounts.UserProfile'
MESSAGE_STORAGE                     = 'django.contrib.messages.storage.session.SessionStorage'
#WSGI_APPLICATION                   = 'wsgi.application'


# Databases
# ==========
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecomdb_0',
        'USER': 'ecomarket',
        'PASSWORD': 'ecomarket',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
            "init_command": "SET storage_engine=INNODB",
        }
    }
}


# Email settings
# ===============

SUPPORT_URL                         = 'http://help.ecomarket.com/'
SUPPORT_EMAIL                       = 'noreply@ecomarket.com'
SERVER_EMAIL                        = SUPPORT_EMAIL
DEFAULT_FROM_EMAIL                  = SUPPORT_EMAIL
DEFAULT_FROM_NAME                   = 'Eco Market'
SEND_BROKEN_LINK_EMAILS             = False


# Apps & Middlewares
# ==================
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'django.contrib.humanize',
    'django.contrib.markup',
    'django.contrib.syndication',
    'django.contrib.comments',

    'annoying',
    'categories.editor',
    'compressor',
    'django_extensions',
    #'debug_toolbar',
    'gunicorn',
    'haystack',
    'social_auth',
    'south',
    'django_nose',
    'storages',  # TODO: When launching, make sure the ajaxuploader in image_crop.views uses the same backend as django-storage
    'pagination',
    'easy_thumbnails',
    'tinymce',
    'actstream',
    'mptt',
    'rollyourown.seo',
    'ckeditor',
    'raven.contrib.django',
    'django_cron',

    'accounts',
    'impersonation',
    'lovelists',
    'main',
    'marketplace',
    'messaging',
    'notifications',
    'purchase',
    'search',
    'todos',
    'articles',
    'image_crop',
    'spamish',
    'threadedcomments',
    'alerts',
    'mailing_lists',
    'social_network',
    'analytics',
    'discounts',
    'sem',
    'djipchat',
    #Deprecate later,
    'product_tmp',
    'monitoring',
)

MIDDLEWARE_CLASSES = (
    'analytics.middlewares.ClicktaleRecordMiddleware',
    'main.middlewares.DomainRedirectMiddleware',
    #'django.middleware.common.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',

    'analytics.middlewares.LifetimeTrackMiddleware',
    'social_auth.middleware.SocialAuthExceptionMiddleware',
    'main.middlewares.SetRemoteAddrFromForwardedFor',
    'main.middlewares.AdminSecretMiddleware',
    'main.middlewares.ExceptionUserInfoMiddleware',
    'main.middlewares.GoogleUtmCookies',
    'minidetector.Middleware',
    'todos.middlewares.TodoMiddleware',
    'purchase.middleware.AnonymousCart',
    'analytics.middlewares.ClicktaleSettingsMiddleware',
    'main.middlewares.UserLocaleMiddleware',
    'accounts.middlewares.SailthruLoginCookie'
)

AUTHENTICATION_BACKENDS = (
    "social_auth.backends.facebook.FacebookBackend",
    "accounts.backends.EmailorUsernameAuthBackend",
    "django.contrib.auth.backends.ModelBackend",
)


# Template settings
# ===============
if DEBUG:
    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )
else:
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )),
    )

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    "django.core.context_processors.request",
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',

    "main.context_processors.globals",
    "accounts.context_processors.account_messages",
    "marketplace.context_processors.categories",
    "messaging.context_processors.inbox",
    "social_network.context_processors.activities_count",
    "purchase.context_processors.has_incomplete_payment_tracking",
)

LOGGER_SIGNALS = "signals_receivers"

# Logging
# =========
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
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False
        },
        'sentry': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        }
    }
}


# Sessions
# ========
# SESSION_ENGINE                      = 'django.contrib.sessions.backends.cached_db'  # BT: Commented out as it was messing up Facebook logins and Django Messages.
SESSION_EXPIRE_AT_BROWSER_CLOSE     = False

# Caching
# =======
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        #'LOCATION': 'unique-snowflake'
    }
}

# Testing
# ========
TEST_RUNNER                         = 'django_nose.NoseTestSuiteRunner'


# Articles
# ===================
ARTICLE_PAGINATION                  = 7
USE_ADDTHIS_BUTTON                  = False

# Marketplace & Stalls
# ===================
STALL_PAGINATION                    = 18

# Comments
# ===================
COMMENTS_APP                        = 'threadedcomments'
COMMENTS_HIDE_REMOVED               = False
APP_COMMENTS_TO_SHOW                = 3

# Analytics
# ==================
GOOGLE_ANALYTICS_PROPERTY_ID        = 'UA-7758350-1'
GOOGLE_ANALYTICS_ENABLED            = False
GOOGLE_ANALYTICS_SITE_NAME          = 'ecomarket.com'

GOOGLE_ADWORDS_ENABLED              = False

# Curebit
# =======
DEFAULT_CUREBIT_SITE_ID             = None

# django-haystack
# ===================
HAYSTACK_CONNECTIONS = {
    'default': {
        #'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'ENGINE': 'search.backend.CustomSolrEngine',
        'URL': 'http://127.0.0.1:8983/solr',
        'TIMEOUT': 60 * 5,
    },
}


# django-registration
# =====================
ACTIVATION_EXPIRATION_DAYS          = 7
LOGIN_REDIRECT_URL                  = '/'
LOGIN_URL                           = '/log-in/'
LOGIN_ERROR_URL                     = '/log-in/?social-login-error=1'
LOGOUT_URL                          = '/accounts/logout/'


# django-social-auth
# =====================
from django.template.defaultfilters import slugify
SOCIAL_AUTH_COMPLETE_URL_NAME       = 'socialauth_complete'
REDIRECT_FIELD_NAME                 = 'next'
SOCIAL_AUTH_ERROR_KEY               = 'social_errors'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL   = '/accounts/new-users-redirect-url/'  # Stall or Normal user selection via register_success
SOCIAL_AUTH_EXPIRATION              = 'expires'
SOCIAL_AUTH_RAISE_EXCEPTIONS        = False
SOCIAL_AUTH_BACKEND_ERROR_URL       = '/accounts/login/'
SOCIAL_AUTH_SLUGIFY_USERNAMES       = True
SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'social_auth.backends.pipeline.associate.associate_by_email',
    'social_auth.backends.pipeline.user.get_username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'accounts.social_auth.create_profile',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details',
    'accounts.social_auth.update_person_details',
)

# Facebook keys
# Goto https://developers.facebook.com/apps and override in your local settings.py
#Staging keys
# FACEBOOK_SITE_NAME                  = 'Ecomarket Staging'
# FACEBOOK_APP_ID                     = '544012218959186'
# FACEBOOK_API_SECRET                 = '62e594a5161e6ac762c286a5f8c08ebe'

#Production keys
FACEBOOK_SITE_NAME                  = 'Eco Market Marketplace App'
FACEBOOK_APP_ID                     = '479432812096685'
FACEBOOK_API_SECRET                 = '5fa2708038000b2a52d3f2e5d3a81430'
FACEBOOK_NAMESPACE                  = 'eco-market'  # 'ecomarket' was taken!

#Will request these both for user and his friends
BASE_PERMISSIONS = [
    'about_me',
    'birthday',
    'hometown',
    'interests',
    'likes',
    'status',
]
BASE_USER_PERMISSIONS = ['email'] + ['user_%s' % perm for perm in BASE_PERMISSIONS]
BASE_FRIEND_PERMISSIONS = ['friends_%s' % perm for perm in BASE_PERMISSIONS]
EXTENDED_PERMISSIONS = ['publish_stream']
#django-social-auth setting
FACEBOOK_EXTENDED_PERMISSIONS       = BASE_USER_PERMISSIONS + BASE_FRIEND_PERMISSIONS + EXTENDED_PERMISSIONS

# Payments
# ===================
PAYPAL_USE_IPN                      = False # TODO: Change to True after modifying purchase/api

PAYPAL_SANDBOX                      = True
PAYPAL_APPLICATION_ID               = 'APP-80W284485P519543T' # sandbox only
PAYPAL_USERID                       = 'tech.alerts_api1.ecomarket.com'
PAYPAL_PASSWORD                     = 'DVY4VC9ZR84BL797'
PAYPAL_SIGNATURE                    = 'ALhGe9cc0fvw81HdHv7K1z4aOaGLAKN1JRX3ABqOwnqykLKCndQgBIYl'
PAYPAL_EMAIL                        = 'tech.alerts@ecomarket.com'

PAYPAL_COMMISION                    = 15
DEFAULT_CURRENCY_CODE               = 'GBP'


# TinyMCE
# ===================
TINYMCE_FILEBROWSER = False
TINYMCE_COMPRESSOR = False
#TINYMCE_JS_URL = '%sgrappelli/tinymce/scripts/tiny_mce/tiny_mce.js' % STATIC_URL
#TINYMCE_JS_ROOT = os.path.join(STATIC_ROOT, 'grappelli/tinymce/scripts/tiny_mce')
TINYMCE_JS_URL = '%stiny_mce/tiny_mce.js' % STATIC_URL
TINYMCE_JS_ROOT = os.path.join(STATIC_ROOT, 'tiny_mce')
TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'plugins': "insertimage,table,paste,searchreplace",
    'theme_advanced_buttons3_add': "insertimage|,spellchecker|,pastetext,pasteword,selectall",
    'theme_advanced_toolbar_location' : "top",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
}


# Django Activity Stream
# ======================
ACTSTREAM_SETTINGS = {
    'MODELS': (
        'auth.user',
        'marketplace.product',
        'marketplace.stall',
        'threadedcomments.threadedcomment',
        'articles.article',
        'accounts.userprofile',
        'lovelists.lovelist',
        'social_network.userfollow',
        'lovelists.lovelistproduct',
        'lovelists.lovelist',
        'purchase.order'
    ),
}


# Miscellaneous
# ===================
ADMIN_SECRET                        = 'morghulis'
ADMIN_SECRET_BLOCK_PATHS            = []
DATABASE_BACKUP_ROOT                = '~/backups/'

# Password hashers
# ===================

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
    'accounts.hashers.JoomlaPasswordHasher',
)


# Caterogies
# ===================
CATEGORIES_SETTINGS = {
    "REGISTER_ADMIN": False,
    "ALLOW_SLUG_CHANGE": True,
}

PAGINATION_DEFAULT_PAGINATION = 20
MIXPANEL_ACTIVE = True
MIXPANEL_TOKEN = '1bb1b11d9f43ed657c829baf6b0d62dc'

# Sailthru
# ===================
SAILTHRU_API_KEY = '' # Unset so testing data doesn't get on Sailthru
SAILTHRU_API_SECRET = ''

# Open Exchange Rates
# ===================
OPENEXCHANGE_RATE_APP_ID = '4d1f9a1528984a9aa1d04c3c44ca08a1'

CRON_CLASSES = [
    'marketplace.cron.CurrencyUpdateCron',
    #'analytics.cron.AggregateUpdateCron',
    #'sem.cron.AdWordsPullCron',
    #'sem.cron.AdWordsManipulateCron',
]

SELLER_FTP_ACCOUNTS = {
    'AMAZON_US': {
        'host': 'productads.amazon-digital-ftp.com',
        'username': 'M_ECOMARKET_13827171',
        'password': 'azPomesz55',
        'filename': 'product_feed_amazon_US.txt'
    },
    'AMAZON_GB': {
        'host': 'dar-eu.amazon-digital-ftp.com',
        'username': 'M_ECOMARKETU_1415317_UK',
        'password': 'T7e2hCAnTg',
        'filename': 'product_feed_amazon_GB.txt'
    },
    'SHOPZILLA_GB': {
        'host': 'ftp.shopzilla.co.uk',
        'username': '281086_hfvWEG',
        'password': 'R6uN1q',
        'filename': 'product_feed_shopzilla_GB.txt'
    },
    'BECOME_US': {
        'host': 'ftp.become.com',
        'username': 'ecomarket',
        'password': 'beaker69',
        'filename': 'product_feed_become_US.txt'
    },
    'THEFIND_GB': {
        'host': 'ftp.thefind.com',
        'username': 'ftp-ecomarket',
        'password': 'T7e2hCAnTg',
        'filename': 'product_feed_thefind_GB.xml'
    },
    'EBAY_GB': {
        'host': 'ftp.ebaycommercenetwork.com',
        'username': 'm517541',
        'password': 'tqxdBRuY',
        'filename': 'product_feed_ebay_GB.xml'
    },
    'NEXTAG_GB': {
        'host': 'upload.nextag.com',
        'username': 'ecomarketuk',
        'password': 'dxxd93',
        'filename': 'product_feed_nextag_GB.csv'
    }
}

# HIPCHAT
HIPCHAT_TOKEN = "3ade33da14978fb748c34d635f9b37"
HIPCHAT_ROOM = "82667"
HIPCHAT_MAIL_ROOM = "308653"
HIPCHAT_VIDEO_ROOM = "82667"

# Cache keys for important caches
CACHE_KEY_ACTIVITIES_COUNT = 'activities_count_%s'
CACHE_KEY_ACTIVITIES = 'activities_%s'

PASSWORD_RESET_TIMEOUT_DAYS = 90

try:
    from local_settings import *
except ImportError:
    pass