"""
Copyright (c) 2015 - present Sdata.ir
"""

from pathlib import Path, os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ------------------------- Configs -------------------------
# ------------------------------------------------------------
SECRET_KEY = os.getenv('SECRET_KEY', 'full_amniat')
DEBUG = os.getenv('DEBUG', True)
DB_ENGINE = os.getenv('DB_ENGINE', 'sqlite3')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

CSRF_TRUSTED_ORIGINS = []

ROOT_URLCONF = "core.urls"


# ----------------- Applications -----------------
# ------------------------------------------------
DEFAULT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
]

LOCAL_APPS = [
    'main',
    'accounts',
    'demo',
    'profiles', 
    'products', 
    'panel',
    'edu',
    'order',
    'payment',
    'ticket',
    'wishlist', 
    'cart',
    'pwa',
]

THIRD_PARTY_APPS = [
    'django_jalali',
    'jalali_date',
    'admin_interface',
    'colorfield',
    "ckeditor",
    "ckeditor_uploader",
    'crispy_forms',
    'widget_tweaks', 
    'azbankgateways',
    'import_export',

]


INSTALLED_APPS = THIRD_PARTY_APPS + LOCAL_APPS + DEFAULT_APPS


# ----------------- Middlewares ------------------
# ------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    # Admin Access 
    'accounts.middlewares.AdminUserMiddleWare',
    # /Admin Access
]


# ----------------- Templates -------------------
# -----------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "products.context_processors.top_professors", 
                "products.context_processors.categories", 
                "products.context_processors.professors", 
                "products.context_processors.packages", 
                "products.context_processors.courses", 
                "products.context_processors.chapters", 
                "products.context_processors.parts", 
                "products.context_processors.users", 
                'products.context_processors.packages_in_orders',
                'products.context_processors.courses_in_orders',
                'wishlist.context_processors.wishlist_count',
                'cart.context_processor.cart', 
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# ------------------------- DATABASE -------------------------
# ------------------------------------------------------------
DATABASES = {
    
}

if DEBUG and DB_ENGINE == 'sqlite3':
    DATABASES['default'] = {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join('db.sqlite3'),
    }
else:
    DATABASES['default'] = {
            'ENGINE': 'django.db.backends.postgresql',
    }



# ------------------ Password validation ---------------------
# ------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]



# ---------------------- Internationalization ----------------------
# ------------------------------------------------------------------
LANGUAGE_CODE = "fa-ir"
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True


# ---------------------- JalaliDateTimeSettings ----------------------
# ------------------------------------------------------------------
# locale.setlocale(locale.LC_ALL, "fa_IR.UTF-8")

# default settings (optional)
JALALI_DATE_DEFAULTS = {
    'Strftime': {
        'date': '%y/%m/%d',
        'datetime': '%H:%M:%S _ %y/%m/%d',
    },
    'Static': {
        'js': [
            # loading datepicker
            'admin/js/django_jalali.min.js',
            # OR
            # 'admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.core.js',
            # 'admin/jquery.ui.datepicker.jalali/scripts/calendar.js',
            # 'admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.datepicker-cc.js',
            # 'admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.datepicker-cc-fa.js',
            # 'admin/js/main.js',
        ],
        'css': {
            'all': [
                'admin/jquery.ui.datepicker.jalali/themes/base/jquery-ui.min.css',
            ]
        }
    },
}
# ------------------------- STATIC -------------------------
# ------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "core/static_files"),
]


# ------------------------- MEDIA -------------------------
# ------------------------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# ------------------- Other Configs --------------------
# ------------------------------------------------------
from django.contrib.messages import constants as messages

AUTH_USER_MODEL = 'accounts.User'

X_FRAME_OPTIONS = 'same-origin'

MESSAGE_TAGS = {
    messages.DEBUG: 'info',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# LOGIN_URL = reverse_lazy('accounts:login')
LOGOUT_REDIRECT_URL = '/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# ckeditor
CKEDITOR_UPLOAD_PATH = "ckeditor/uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
    },
}
# CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
# /ckeditor


DEFAULT_PAGINATE_NUMBER = 10


# ------------------------- EMAIL -------------------------
# ------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.getenv('EMAIL_PORT', '')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')


# ------------------------- REXAN API CONFIGS ----------------
# ------------------------------------------------------------
RESERVATION_API_BASE_URL = os.getenv('API_BASE_URL', 'https://rexan.megagasht.ir')
RESERVATION_API_KEY = os.getenv('RESERVATION_API_KEY', 'testapikey')


# ------------------- SECURITY CONFIGS -------------------
# --------------------------------------------------------
if not bool(DEBUG):
    # security.W016
    CSRF_COOKIE_SECURE = True

    # security.W012
    SESSION_COOKIE_SECURE = True


    # security.W004
    SECURE_HSTS_SECONDS = 31536000 # One year in seconds


    # Another security settings
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # SECURE_HSTS_PRELOAD = True
    # SECURE_CONTENT_TYPE_NOSNIFF = True

KAVENEGAR_API_KEY = os.getenv('KAVENEGAR_API_KEY', '43797135366B4D7754506454527153616E6933526769585538762F4D78774E7761477951595338693450633D')
CRISPY_TEMPLATE_PACK = 'bootstrap4' 



MERCHANT_ID = '6f1c037a-537d-4f15-86b6-87a1001f0483'

# if os.getenv('DB_ENGINE', 'DB_ENGINE is not set.') == 'sqlite3' and os.getenv('DEBUG'):
#     gateway_callback_url = 'http://127.0.0.1:8000/payment/verify/'
# else:
#     gateway_callback_url = 'https://Safir-edu.sdata.ir/payment/verify/'

# ZARINPAL = {
#     'gateway_request_url': 'https://www.zarinpal.com/pg/services/WebGate/wsdl',
#     'gateway_callback_url': gateway_callback_url,
#     'merchant_id': MERCHANT_ID
# }


AZ_IRANIAN_BANK_GATEWAYS = {
   'GATEWAYS': {
       'SEP': {
           'MERCHANT_CODE': '14181170',
           'TERMINAL_CODE': '14181170',
       },
   },
   'DEFAULT': 'SEP',
   "TRACKING_CODE_QUERY_PARAM": "tc",  # اختیاری
   "TRACKING_CODE_LENGTH": 16,  # اختیاری
  
}


CART_SESSION_ID = 'cart'


SABANOVIN_SMS_API_KEY = os.getenv('SABANOVIN_SMS_API_KEY', 'sa2081349585:RACVmnUmHAvdNeHcMxYnWUw9lLDW3JoanYg1')
SABANOVIN_SMS_GATEWAY = os.getenv('SABANOVIN_SMS_GATEWAY', '90003002')


# ------------------------- CRONJOBS -------------------------
# ------------------------------------------------------------
# CRONJOBS = [
#     ('0 20 * * *', 'profiles.management.commands.check_remaining_days'), # every day in 20:00
# ]

PWA_APP_NAME = 'Safirmall'
PWA_APP_DESCRIPTION = "آموزش زبان"
PWA_APP_THEME_COLOR = '#0f2741'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
	{
		'src': '/static/logo-new.png',
		'sizes': '160x160'
	}
    
]

PWA_APP_ICONS_APPLE = [
	{
		'src': '/static/logo-new.png',
		'sizes': '160x160'
	}
]

PWA_APP_SPLASH_SCREEN = [
	{
		'src': '/static/logo-new.png',
		'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
	}
]
PWA_APP_DIR = 'rtl'
PWA_APP_LANG = 'fa-IR'