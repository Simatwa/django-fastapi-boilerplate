from django.db import models
from users.models import CustomUser
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from project.utils import EnumWithChoices
from ckeditor.fields import RichTextField

# Create your models here.


class MessageCategory(EnumWithChoices):
    GENERAL = "General"
    PAYMENT = "Payment"
    MAINTENANCE = "Maintenance"
    PROMOTION = "Promotion"
    WARNING = "Warning"
    OTHER = "Other"


class MemberGroup(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        help_text=_("Name of the members' group"),
        null=False,
        blank=False,
    )
    description = RichTextField(
        verbose_name=_("Description"),
        help_text=_("Description of the user group"),
        null=True,
        blank=True,
    )
    social_media_link = models.URLField(
        verbose_name=_("Social media link"),
        help_text=_("Link to online forum for members"),
        max_length=200,
        null=True,
        blank=True,
    )
    members = models.ManyToManyField(
        CustomUser,
        verbose_name=_("Members"),
        help_text=_("Users who are members of this group"),
        related_name="member_groups",
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Member Group")
        verbose_name_plural = _("Member Groups")


class GroupMessage(models.Model):
    groups = models.ManyToManyField(
        MemberGroup,
        verbose_name=_("Groups"),
        help_text=_("User-Groups to receive this message"),
        related_name="group_messages",
    )

    category = models.CharField(
        max_length=20,
        choices=MessageCategory.choices(),
        default=MessageCategory.GENERAL.value,
        verbose_name=_("Category"),
        help_text=_("Category of the message"),
        null=False,
        blank=False,
    )
    subject = models.CharField(
        max_length=200,
        verbose_name=_("Subject"),
        help_text=_("Message subject"),
        null=False,
        blank=False,
    )
    content = RichTextField(
        verbose_name=_("Content"),
        help_text=_("Message in details"),
        null=False,
        blank=False,
    )
    read_by = models.ManyToManyField(
        CustomUser,
        blank=True,
        verbose_name=_("Read by"),
        help_text=_("Users who have read this message"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("Date and time when the message was created"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
        help_text=_("Date and time when the message was last updated"),
    )

    def model_dump(self):
        return dict(
            id=self.id,
            category=self.category,
            subject=self.subject,
            content=self.content,
            created_at=self.created_at,
        )

    class Meta:
        verbose_name = _("Group Message")
        verbose_name_plural = _("Group Messages")

    def __str__(self):
        return f"{self.subject} ({self.category})"


class PersonalMessage(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        help_text=_("Receiver of the message"),
        related_name="messages",
    )
    category = models.CharField(
        max_length=20,
        choices=MessageCategory.choices(),
        default=MessageCategory.GENERAL.value,
        verbose_name=_("Category"),
        help_text=_("Category of the message"),
    )
    subject = models.CharField(
        max_length=200,
        verbose_name=_("Subject"),
        help_text=_("Message subject"),
        null=False,
        blank=False,
    )
    content = RichTextField(
        verbose_name=_("Content"),
        help_text=_("Message in details"),
        null=False,
        blank=False,
    )
    is_read = models.BooleanField(
        verbose_name=_("Is read"), default=False, help_text=_("Message read status")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("Date and time when the entry was created"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
        help_text=_("Date and time when the entry was last updated"),
    )

    class Meta:
        verbose_name = _("Personal Message")
        verbose_name_plural = _("Personal Messages")

    def __str__(self):
        return f"{self.subject} ({self.category}) - {self.user}"


class Concern(models.Model):
    class ConcernStatus(EnumWithChoices):
        OPEN = "Open"
        IN_PROGRESS = "In Progress"
        RESOLVED = "Resolved"
        CLOSED = "Closed"

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        help_text=_("Person raising this concern"),
        related_name="concerns",
    )
    about = models.CharField(max_length=200, verbose_name=_("About"), help_text=_("Main issue being raised."))
    details = models.TextField(verbose_name=_("Details"), help_text=_("Concern in details"))
    response = RichTextField(
        verbose_name=_("Response"),
        help_text=_("Feedback from the concerned body"),
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=ConcernStatus.choices(),
        default=ConcernStatus.OPEN.value,
        verbose_name=_("Status"),
        help_text=_("Current status of the concern"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
        help_text=_("Date and time when the entry was last updated"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("Date and time when the entry was created"),
    )

    def model_dump(self):
        return dict(
            id=self.id,
            about=self.about,
            details=self.details,
            response=self.response,
            status=self.status,
            updated_at=self.updated_at,
            created_at=self.created_at,
        )

    class Meta:
        verbose_name = _("Member Concern")
        verbose_name_plural = _("Member Concerns")

    def __str__(self):
        return f"{self.about} - {self.user} - {self.status}"

    # TODO: Mail user about changes on status


class AppUtility(models.Model):
    """Utility data for the application such currency"""

    class UtilityName(EnumWithChoices):
        CURRENCY = "Currency"
        LIBRARY_OPENING_HOURS = "Library Opening Hours"
        LIBRARY_CLOSING_HOURS = "Library Closing Hours"
        BOOKS_BORROWING_LIMIT = "Books borrowing limit"

    name = models.CharField(
        max_length=30,
        verbose_name=_("Name"),
        choices=UtilityName.choices(),
        help_text=_("Name of this utility"),
        null=False,
        blank=False,
        unique=True,
    )
    description = RichTextField(
        verbose_name=_("Description"),
        help_text=_("Description of this app utility"),
        null=False,
        blank=False,
    )
    value = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name=_("Value"),
        help_text=_("Value for this utility"),
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
        return f"{self.name} - {self.value}"

    class Meta:
        verbose_name = _("App Utility")
        verbose_name_plural = _("App Utilities")
