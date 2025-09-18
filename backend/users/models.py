from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.core.validators import FileExtensionValidator
from django.core.validators import RegexValidator
from django.utils import timezone
from project.utils import get_expiry_datetime
from finance.models import UserAccount
from project.utils import EnumWithChoices, generate_document_filepath
from django.utils import timezone

# Create your models here.


class CustomUser(AbstractUser):
    class UserGender(EnumWithChoices):
        MALE = "M"
        FEMALE = "F"
        OTHER = "O"

    date_of_birth = models.DateField(
        verbose_name=_("Date of birth"),
        help_text=_("User's date of birth"),
        default="2000-01-01",
    )

    gender = models.CharField(
        verbose_name=_("gender"),
        max_length=10,
        help_text=_("Select one"),
        choices=UserGender.choices(),
        default=UserGender.OTHER.value,
    )

    address = models.CharField(
        max_length=30,
        verbose_name=_("Address"),
        help_text=_("User's location address"),
        null=False,
        blank=False,
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name=_("Phone number"),
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message=_(
                    "Phone number must be entered in the format: '+254...' or '07...'. Up to 15 digits allowed."
                ),
            )
        ],
        help_text=_("Contact phone number"),
        blank=False,
        null=False,
    )

    profile = models.ImageField(
        _("Profile Picture"),
        default="default/user.png",
        upload_to=generate_document_filepath,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
        blank=True,
        null=True,
    )
    account = models.OneToOneField(
        UserAccount,
        on_delete=models.RESTRICT,
        help_text=_("Finance account"),
        related_name="user",
    )

    token = models.CharField(
        _("token"),
        help_text=_("User auth token"),
        null=True,
        blank=True,
        max_length=40,
        unique=True,
    )
    # USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ("email",)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def save(self, *args, **kwargs):
        if not self.id:  # new entry
            if len(self.password) < 50:
                # TODO: Implement your own logic for differenciating hashed and unhashed passwords
                self.set_password(self.password)
            new_account = UserAccount.objects.create()
            new_account.save()
            self.account = new_account
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    @property
    def age(self):
        return timezone.now().date().year - self.date_of_birth.year

    def model_dump(self):
        return dict(
            first_name=self.first_name,
            last_name=self.last_name,
            date_of_birth=self.date_of_birth,
            gender=self.gender,
            address=self.address,
            phone_number=self.phone_number,
            email=self.email,
            username=self.username,
            account_balance=self.account.balance,
            profile=self.profile.url,
            is_staff=self.is_staff,
            date_joined=self.date_joined,
        )


class AuthToken(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="auth_token")
    token = models.CharField(help_text=_("auth token value"), max_length=80, null=False)
    expiry_datetime = models.DateTimeField(
        help_text=_("Expiry datetime"), null=False, default=get_expiry_datetime
    )

    def is_expired(self):
        return timezone.now() > self.expiry_datetime
