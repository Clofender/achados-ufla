import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-local-development-only",
)
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
    "occurrences",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

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

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

JAZZMIN_SETTINGS = {
    "site_title": "Achados UFLA | Administração",
    "site_header": "Achados UFLA",
    "site_brand": "Achados UFLA",
    "site_logo": "core/img/achados-ufla.svg",
    "site_logo_classes": "",
    "site_icon": "core/img/achados-ufla.svg",
    "welcome_sign": "Administração de objetos perdidos e encontrados",
    "copyright": "Achados UFLA",
    "custom_css": "core/css/admin.css",
    "use_google_fonts_cdn": False,
    "show_sidebar": True,
    "navigation_expanded": True,
    "topmenu_links": [
        {"name": "Início", "url": "admin:index"},
        {"model": "core.Item"},
        {"model": "occurrences.Occurrence"},
    ],
    "order_with_respect_to": [
        "core",
        "core.Item",
        "core.Category",
        "core.Location",
        "occurrences",
        "auth",
    ],
    "icons": {
        "core": "fas fa-search",
        "core.Item": "fas fa-box-open",
        "core.Category": "fas fa-tags",
        "core.Location": "fas fa-map-marker-alt",
        "occurrences": "fas fa-clipboard-list",
        "occurrences.Occurrence": "fas fa-clipboard-list",
        "auth": "fas fa-users-cog",
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    "show_ui_builder": False,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "default_theme_mode": "auto",
    "brand_colour": "bg-success text-white",
}
