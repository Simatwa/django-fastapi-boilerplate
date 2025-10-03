from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from project.utils.models import crop_image_to_ratio, remove_file_from_system

from users.models import DEFAULT_PROFILE, CustomUser


@receiver(pre_delete, sender=CustomUser)
def auto_delete_profile_img(sender, instance: CustomUser, **kwargs):
    if instance.profile.name != DEFAULT_PROFILE:
        remove_file_from_system(instance.profile)


@receiver(pre_save, sender=CustomUser)
def crop_and_compress_profile_img(sender, instance: CustomUser, **kwargs):
    if not instance.profile:
        instance.profile.name = DEFAULT_PROFILE

    elif (
        instance.profile.name != DEFAULT_PROFILE
        and not instance.profile._committed
    ):
        instance.profile = crop_image_to_ratio(
            instance.profile, target_width=256, target_height=256
        )
