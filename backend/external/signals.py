from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from project.utils import remove_file_from_system
from project.utils.models import convert_to_webp

from external.models import DEFAULT_LOGO, DEFAULT_WALLPAPER, About, Gallery


@receiver(pre_delete, sender=Gallery)
def auto_delete_gallery_pic(sender, instance: Gallery, **kwargs):
    remove_file_from_system(instance.picture)


@receiver(pre_save, sender=Gallery)
def auto_webp_gallery_pic(sender, instance: Gallery, **kwargs):
    if instance.picture and instance.picture._committed is False:
        instance.picture = convert_to_webp(instance.picture)


@receiver(pre_delete, sender=About)
def auto_delete_logo_and_cover(sender, instance: About, **kwargs):
    for entry in filter(
        lambda v: v.name != DEFAULT_LOGO and v.name != DEFAULT_WALLPAPER,
        {instance.logo, instance.wallpaper},
    ):
        remove_file_from_system(entry)


@receiver(pre_save, sender=About)
def ensure_logo_and_wallpaper_not_empty(sender, instance: About, **kwargs):
    # also does the compression
    if not instance.logo:
        instance.logo.name = DEFAULT_LOGO

    elif (
        instance.logo.name != DEFAULT_LOGO and instance.logo._committed is False
    ):
        instance.logo = convert_to_webp(instance.logo)

    if not instance.wallpaper:
        instance.wallpaper.name = DEFAULT_WALLPAPER

    elif (
        instance.wallpaper.name != DEFAULT_WALLPAPER
        and instance.wallpaper._committed is False
    ):
        instance.wallpaper = convert_to_webp(instance.wallpaper)
