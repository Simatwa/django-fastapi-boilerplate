from pydantic import BaseModel, HttpUrl, field_validator
from typing import Literal, Optional, Annotated  #
from envist import Envist


class EnvSettings(BaseModel):
    """Projects's config parsed from .env file"""

    DATABASE_ENGINE: Literal[
        "django.db.backends.mysql",
        "django.db.backends.postgresql",
        "django.db.backends.sqlite3",
        "django.db.backends.oracle",
    ] = "django.db.backends.sqlite3"
    DATABASE_NAME: Optional[str] = "db.sqlite3"
    DATABASE_USER: str = "developer"
    DATABASE_PASSWORD: str = "development"
    DATABASE_HOST: Optional[str] = "localhost"
    DATABASE_PORT: Optional[int] = 3306

    # APPLICATION
    SECRET_KEY: Optional[str] = "django-insecure-%sx#6ax4gpycp&ixq9ejj*wwtdk&#g)5@nyhp)4)_9h)h!$@kw"
    DEBUG: Optional[bool] = True
    ALLOWED_HOSTS: Optional[list[str]] = ["*"]
    LANGUAGE_CODE: Optional[str] = "en-us"
    TIME_ZONE: Optional[str] = "Africa/Nairobi"
    SITE_NAME: Optional[str] = "MySite"
    SITE_ADDRESS: Annotated[str, HttpUrl] = "http://localhost:8000"
    FRONTEND_DIR: Optional[str] = None

    # E-MAIL
    EMAIL_BACKEND: Optional[str] = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST: Optional[str] = "smtp.gmail.com"
    EMAIL_PORT: Optional[int] = 587
    EMAIL_USE_TLS: Optional[bool] = True
    EMAIL_HOST_USER: str
    EMAIL_HOST_PASSWORD: str = None  # Your email password or app-specific password
    DEFAULT_FROM_EMAIL: str = None  # Optional: default sender email

    # CORS
    CORS_ALLOWED_ORIGINS: list[str] = []
    CORS_ALLOWED_ORIGIN_REGEXES: list[str] = []
    CORS_ALLOW_ALL_ORIGINS: Optional[bool] = False

    # UTILS
    CURRENCY: Optional[str] = "Ksh"

    DEMO: Optional[bool] = False

    # PROJECT
    REPOSITORY_LINK: Optional[str] = "https://github.com/Simatwa/django-fastapi-boilerplate"
    LICENSE: Optional[str] = "Unspecified"

    API_PREFIX: Optional[str] = "/api"

    @field_validator("API_PREFIX")
    def validate_api_prefix(value: str):
        if not value.startswith("/"):
            value = "/" + value
        return value


env_setting = EnvSettings(**Envist().get_all())
