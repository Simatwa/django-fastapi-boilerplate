"""Provides common required functions and classes"""

import random
from datetime import datetime, timedelta
from enum import Enum
from os import path
from string import ascii_uppercase, digits

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from project import settings


def generate_document_filepath(instance, filename: str) -> str:
    filename, extension = path.splitext(filename)
    return (
        f"{instance.__class__.__name__.lower()}/{filename}_{instance.id or ''}"
        f"{extension}"
    )


def send_email(
    subject: str, message: str, recipient: str, html_message: str = None
):
    if settings.EMAIL_HOST_PASSWORD is None:
        return
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient],
        fail_silently=(not settings.DEBUG),  # Silent in production
        html_message=html_message,
    )


def send_email_from_template(
    subject: str, template_name: str, context: dict, recipient: str
):
    context.update(
        {
            "site_name": settings.SITE_NAME,
            "year": timezone.now().year,
            "date": timezone.now().date(),
        }
    )
    html_message = render_to_string(
        template_name=template_name, context=context
    )
    return send_email(
        subject=subject,
        message="",
        recipient=recipient,
        html_message=html_message,
    )


def get_expiry_datetime(minutes: float = 30) -> datetime:
    return timezone.now() + timedelta(minutes=minutes)


def generate_random_token(length: int = 8) -> str:
    population = list(ascii_uppercase + digits)
    return "".join(random.sample(population, length))


def format_datetime(date_time: datetime) -> str:
    return date_time.strftime("%B %d, %Y, %I:%M %p")


class EnumWithChoices(Enum):
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
