from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from project.utils.models import (
    crop_image_to_ratio,
    is_image_processed,
    remove_file_if_possible,
)

from users.models import DEFAULT_PROFILE, CustomUser


@receiver(pre_delete, sender=CustomUser)
def auto_delete_profile_img(sender, instance: CustomUser, **kwargs):
    remove_file_if_possible(instance.profile, DEFAULT_PROFILE)


@receiver(pre_save, sender=CustomUser)
def crop_and_compress_profile_img(sender, instance: CustomUser, **kwargs):
    if not is_image_processed(instance.profile, DEFAULT_PROFILE):
        instance.profile = crop_image_to_ratio(
            instance.profile, target_width=256, target_height=256
        )
