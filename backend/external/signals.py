from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from project.utils.models import (
    convert_to_webp,
    is_image_processed,
    remove_file_if_possible,
)

from external.models import DEFAULT_LOGO, DEFAULT_WALLPAPER, About, Gallery


@receiver(pre_delete, sender=Gallery)
def auto_delete_gallery_pic(sender, instance: Gallery, **kwargs):
    remove_file_if_possible(instance.picture)


@receiver(pre_save, sender=Gallery)
def auto_webp_gallery_pic(sender, instance: Gallery, **kwargs):
    if not is_image_processed(instance.picture):
        instance.picture = convert_to_webp(instance.picture)


@receiver(pre_delete, sender=About)
def auto_delete_logo_and_cover(sender, instance: About, **kwargs):
    remove_file_if_possible(instance.logo, DEFAULT_LOGO)
    remove_file_if_possible(instance.wallpaper, DEFAULT_WALLPAPER)


@receiver(pre_save, sender=About)
def ensure_logo_and_wallpaper_not_empty(sender, instance: About, **kwargs):
    # also does the compression
    if not is_image_processed(instance.logo, DEFAULT_LOGO):
        instance.logo = convert_to_webp(instance.logo)

    if not is_image_processed(instance.wallpaper, DEFAULT_WALLPAPER):
        instance.wallpaper = convert_to_webp(instance.wallpaper)
