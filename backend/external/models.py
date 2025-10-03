from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from project.settings import env_setting
from project.utils import generate_document_filepath
from project.utils.models import (
    DumpableModelCloudFileSupport,
    DumpableModelMixin,
)
from users.models import CustomUser

from external._enums import DocumentName, FeedbackRate, SenderRole

# Create your models here.

DEFAULT_LOGO = "default/logo.png"
DEFAULT_WALLPAPER = "default/wallpaper.jpg"


class About(DumpableModelMixin):
    name = models.CharField(
        max_length=40, help_text="The brand name", default="Library MS"
    )
    short_name = models.CharField(
        max_length=30, help_text="Brand abbreviated name", default="LMS"
    )
    slogan = models.TextField(
        help_text=_("Brand's slogan"),
        default="Empowering knowledge through seamless library management.",
    )
    details = models.TextField(
        help_text=_("Business entity details"),
        default=(
            "Welcome to our Library Management System. We are committed to"
            "enhancing library operations and improving user experiences."
        ),
        null=False,
        blank=False,
    )
    address = models.CharField(
        max_length=200,
        help_text=_("Business address"),
        default="456 Estate Avenue, Nairobi - Kenya",
    )

    founded_in = models.DateField(
        help_text=_("Date when the business was founded"),
        default=timezone.now,
    )
    email = models.EmailField(
        max_length=50,
        help_text="Website's admin email",
        null=True,
        blank=True,
        default="admin@business.com",
    )
    phone_number = models.CharField(
        max_length=50,
        help_text="Business' hotline number",
        null=True,
        blank=True,
        default="0200000000",
    )
    facebook = models.URLField(
        max_length=100,
        help_text=_("Business' Facebook profile link"),
        null=True,
        blank=True,
        default="https://www.facebook.com/",
    )
    twitter = models.URLField(
        max_length=100,
        help_text=_("Business' X (formerly Twitter) profile link"),
        null=True,
        blank=True,
        default="https://www.x.com/",
    )
    linkedin = models.URLField(
        max_length=100,
        help_text=_("Business' Facebook profile link"),
        null=True,
        blank=True,
        default="https://www.linkedin.com/",
    )
    instagram = models.URLField(
        max_length=100,
        help_text=_("Business' Instagram profile link"),
        null=True,
        blank=True,
        default="https://www.instagram.com/",
    )
    tiktok = models.URLField(
        max_length=100,
        help_text=_("Business' Tiktok profile link"),
        null=True,
        blank=True,
        default="https://www.tiktok.com/",
    )
    youtube = models.URLField(
        max_length=100,
        help_text=_("Business' Youtube profile link"),
        null=True,
        blank=True,
        default="https://www.youtube.com/",
    )
    logo = models.ImageField(
        help_text=_("Library logo  (preferrably 64*64px png)"),
        upload_to=generate_document_filepath,
        default=DEFAULT_LOGO,
        blank=True,
        null=False,
    )
    wallpaper = models.ImageField(
        help_text=_("Site wallpaper"),
        upload_to=generate_document_filepath,
        default=DEFAULT_WALLPAPER,
        blank=True,
        null=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("updated at"),
        help_text=_("Date and time when the entry was updated"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created at"),
        help_text=_("Date and time when the entry was created"),
    )

    def __str__(self):
        return self.name


class ServiceFeedback(DumpableModelMixin):
    sender = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        help_text=_("Feedback sender"),
        related_name="feedback",
    )
    message = models.TextField(help_text=_("Response body"))
    rate = models.CharField(
        max_length=15,
        choices=FeedbackRate.choices(),
        help_text=_("Feedback rating"),
    )
    sender_role = models.CharField(
        max_length=40,
        help_text=_("Sender's role/category"),
        choices=SenderRole.choices(),
        default=SenderRole.CUSTOMER.value,
    )
    show_in_index = models.BooleanField(
        default=False,
        help_text=_("Display this feedback in website's testimonials section."),
    )
    list_index = models.IntegerField(
        help_text=_("Index of the feedback in listing"), default=1
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("updated at"),
        help_text=_("Date and time when the entry was updated"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created at"),
        help_text=_("Date and time when the entry was created"),
    )

    class Meta:
        verbose_name = _("Feedback")
        verbose_name_plural = _("Feedbacks")

    def __str__(self):
        return f"{self.rate} feedback from {self.sender}"


class Message(DumpableModelMixin):
    sender = models.CharField(
        verbose_name=_("Sender"),
        max_length=50,
        help_text=_("Sender's name"),
    )
    email = models.EmailField(
        verbose_name=_("Email"),
        max_length=80,
        help_text=_("Sender's email address"),
    )
    body = models.TextField(
        verbose_name=_("Message"), help_text=_("Message body")
    )
    is_read = models.BooleanField(
        verbose_name=_("Is read"),
        help_text=_("Message read status"),
        default=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created at"),
        help_text=_("Date and time when the entry was created"),
    )

    def __str__(self):
        return (
            f"from {self.sender} at "
            f"{self.created_at.strftime('%d-%b-%Y %H:%M:%S')}"
        )


class FAQ(DumpableModelMixin):
    question = models.CharField(
        verbose_name=_("Question"),
        max_length=100,
        help_text=_("The question"),
    )
    answer = models.TextField(
        verbose_name=_("Answer"), help_text=_("Answer to the question")
    )
    index = models.IntegerField(help_text=_("Listing index"), default=0)
    is_shown = models.BooleanField(
        verbose_name="Is shown",
        help_text=_("Show this FAQ in website"),
        default=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created at"),
        help_text=_("Date and time when the entry was created"),
    )

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")


class Gallery(DumpableModelMixin):
    title = models.CharField(max_length=50, help_text=_("Gallery title"))
    details = models.TextField(help_text=_("What about this gallery?"))
    location_name = models.CharField(
        max_length=100,
        help_text=_("Event location name"),
        default=env_setting.SITE_NAME,
    )
    picture = models.ImageField(
        help_text=_("Gallery photograph"),
        upload_to=generate_document_filepath,
        null=True,
        blank=True,
    )
    youtube_video_link = models.URLField(
        max_length=100,
        help_text=_("YouTube video link"),
        null=True,
        blank=True,
    )
    date = models.DateField(help_text="Gallery date", default=timezone.now)
    show_in_index = models.BooleanField(
        default=True,
        help_text=_("Display this gallery in website's gallery section."),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("updated at"),
        help_text=_("Date and time when the entry was updated"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created at"),
        help_text=_("Date and time when the entry was created"),
    )

    def __str__(self):
        return f"{self.title} in {self.location_name} on {self.date}"

    class Meta:
        verbose_name = _("Gallery")
        verbose_name_plural = _("Galleries")


class Document(DumpableModelMixin):
    name = models.CharField(
        max_length=30,
        verbose_name="name",
        choices=DocumentName.choices(),
        help_text=_("Document name"),
        null=False,
        blank=False,
    )
    content = RichTextField(
        verbose_name="Content",
        help_text=_("Document content"),
        null=False,
        blank=False,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("updated at"),
        help_text=_("Date and time when the entry was updated"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created at"),
        help_text=_("Date and time when the entry was created"),
    )

    def __str__(self):
        return f"{self.name} ({self.id})"

    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")
