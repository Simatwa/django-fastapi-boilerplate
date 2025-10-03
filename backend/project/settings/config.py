from typing import Annotated, Literal

from envist import Envist
from pydantic import BaseModel, HttpUrl, field_validator


class EnvSettings(BaseModel):
    """Projects's config parsed from .env file"""

    DATABASE_ENGINE: Literal[
        "django.db.backends.mysql",
        "django.db.backends.postgresql",
        "django.db.backends.sqlite3",
        "django.db.backends.oracle",
    ] = "django.db.backends.sqlite3"
    DATABASE_NAME: str | None = "db.sqlite3"
    DATABASE_USER: str = "developer"
    DATABASE_PASSWORD: str = "development"
    DATABASE_HOST: str | None = "localhost"
    DATABASE_PORT: int | None = 5432

    # APPLICATION
    SECRET_KEY: str | None = (
        "django-insecure-%sx#6ax4gpycp&ixq9ejj*wwtdk&#g)5@nyhp)4)_9h)h!$@kw"
    )
    DEBUG: bool | None = True
    ALLOWED_HOSTS: list[str] | None = ["*"]
    LANGUAGE_CODE: str | None = "en-us"
    TIME_ZONE: str | None = "Africa/Nairobi"
    SITE_NAME: str | None = "MySite"
    SITE_ADDRESS: Annotated[str, HttpUrl] = "http://localhost:8000"
    API_VERSION: str | None = "0.1.0"
    FRONTEND_DIR: str | None = None

    # E-MAIL
    EMAIL_BACKEND: str | None = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST: str | None = "smtp.gmail.com"
    EMAIL_PORT: int | None = 587
    EMAIL_USE_TLS: bool | None = True
    EMAIL_HOST_USER: str
    EMAIL_HOST_PASSWORD: str = (
        None  # Your email password or app-specific password
    )
    DEFAULT_FROM_EMAIL: str = None  # Optional: default sender email

    # CORS
    CORS_ALLOWED_ORIGINS: list[str] = []
    CORS_ALLOWED_ORIGIN_REGEXES: list[str] = []
    CORS_ALLOW_ALL_ORIGINS: bool | None = False
    CORS_ALLOW_METHODS: list[
        Literal[
            "DELETE",
            "GET",
            "HEAD",
            "OPTIONS",
            "PATCH",
            "POST",
            "PUT",
        ]
    ] = [
        "DELETE",
        "GET",
        "HEAD",
        "OPTIONS",
        "PATCH",
        "POST",
        "PUT",
    ]
    CORS_ALLOW_CREDENTIALS: bool | None = False
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    # UTILS
    CURRENCY: str | None = "Ksh"

    DEMO: bool | None = False

    # PROJECT
    REPOSITORY_LINK: str | None = (
        "https://github.com/Simatwa/django-fastapi-boilerplate"
    )
    LICENSE: str | None = "Unspecified"

    API_PREFIX: str | None = "/api"
    DJANGO_PREFIX: str | None = "/d"

    TURNSTILE_SITE_KEY: str | None = None
    TURNSTILE_SECRET_KEY: str | None = None

    #  Cloudstorage
    CLOUDSTORAGE_URL: None | HttpUrl = None
    CLOUDSTORAGE_TOKEN: str | None = None
    DELETE_LOCALFILE: bool = False

    @field_validator(
        "CORS_ALLOWED_ORIGINS",
        "CORS_ALLOWED_ORIGIN_REGEXES",
        "ALLOWED_HOSTS",
        "CORS_ALLOW_METHODS",
        "CORS_ALLOW_HEADERS",
        mode="before",
    )
    def strip_list_elements(values: str):
        if values:
            values = [element.strip() for element in values]
        return values

    @field_validator("API_PREFIX", "DJANGO_PREFIX")
    def validate_route_prefixes(value: str):
        if not value.startswith("/"):
            raise ValueError(
                "Value for route prefix must start with / (forward slash)"
            )
        if value.endswith("/"):
            value = value[:-1]

        return value

    @property
    def cors_allowed_origins(self):
        return self.CORS_ALLOWED_ORIGINS or ["*"]


env_setting = EnvSettings(**Envist().get_all())
