import os
import warnings
from io import BytesIO
from pathlib import Path
from typing import Literal

from django.core.files.base import ContentFile
from django.db import models
from django.db.models import FileField, ImageField
from django.db.models.fields.related import ForeignKey, OneToOneField
from model_utils import FieldTracker
from PIL import Image

from project.utils import cloud_storage

RelationPath = str

IMAGE_FILENAME_PREFIX = (
    "x_prcsd-"  # TODO: Change this to anything of your choice
)


def _get_image_filename(
    original_name: str, final_format: str, prefix: str = IMAGE_FILENAME_PREFIX
) -> str:
    return f"{prefix}{original_name}.{final_format.lower()}"


def is_image_processed(
    image: ImageField,
    default: str = None,
    name_prefix: str = IMAGE_FILENAME_PREFIX,
) -> bool:
    """Whether saved instance.field has ever hit any image processing function
    of this module. If EMPTY set the default as its value.name

    Args:
        image (ImageField): Image field
        default (str, optional): Default field value. Defaults to None.
        name_prefix (str, optional). Defaults to IMAGE_FILENAME_PREFIX.

    Returns:
        bool
    """
    if image:
        if default and image.name == default:
            return True

        return Path(image.name).name.startswith(name_prefix)

    elif default:
        image.name = default

    return True  # Avoid processing none


def remove_file_from_system(
    field: ImageField | FileField,
) -> tuple[bool, Exception | None]:
    """Remove file from system if exists and return success status"""
    try:
        if field:
            os.remove(field.path)

        return (True, None)

    except Exception as e:
        return (False, e)


def can_remove_file(
    field: ImageField | FileField,
    default: str = None,
) -> bool:
    """Whether field value can be removed

    Args:
        field (ImageField | FileField): Field value
        default (str, optional): Default field value. Defaults to None.

    Returns:
        bool
    """
    if field:
        if default:
            return field.name != default
        return True

    return False


def remove_file_if_possible(
    field: ImageField | FileField,
    default: str = None,
) -> None:
    """Checks whether file can be removed. If yes remove it.

    Args:
        field (ImageField | FileField): Field to check against.
        default (str, optional): Default field.name. Defaults to None.
    """
    if can_remove_file(field, default):
        remove_file_from_system(field)


def resize_image(
    image_field: ImageField,
    max_width=800,
    max_height=800,
    img_format: Literal["DEFAULT", "WEBP"] | str = "WEBP",
    quality: int = 85,
):
    """
    Resize an image to fit within max_width and max_height while maintaining
    aspect ratio. Returns a Django ContentFile ready to save to an ImageField.
    """
    img = Image.open(image_field)

    final_format = img.format if img_format == "DEFAULT" else img_format

    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

    buffer = BytesIO()
    img.save(buffer, format=final_format, optimize=True, quality=quality)

    original_name = Path(image_field.name).stem
    new_name = _get_image_filename(original_name, final_format)
    return ContentFile(buffer.getvalue(), name=new_name)


def crop_image_to_ratio(
    image_field: ImageField,
    target_width: int = 256,
    target_height: int = 256,
    img_format: Literal["DEFAULT", "WEBP"] | str = "WEBP",
    quality: int = 85,
) -> ContentFile:
    """
    Crop an image to the target ratio (e.g. 256x256) and resize.
    Returns a Django ContentFile ready to save to an ImageField.

    Example:
        instance.avatar = crop_image_to_ratio(instance.avatar, 256, 256)
    """
    img = Image.open(image_field)
    width, height = img.size
    target_ratio = target_width / target_height
    current_ratio = width / height

    if current_ratio > target_ratio:  # too wide
        new_width = int(height * target_ratio)
        left = (width - new_width) // 2
        right = left + new_width
        top, bottom = 0, height
    else:  # too tall
        new_height = int(width / target_ratio)
        top = (height - new_height) // 2
        bottom = top + new_height
        left, right = 0, width

    img_cropped = img.crop((left, top, right, bottom))
    img_resized = img_cropped.resize(
        (target_width, target_height), Image.Resampling.LANCZOS
    )

    final_format = img.format if img_format == "DEFAULT" else img_format

    buffer = BytesIO()
    img_resized.save(
        buffer, format=final_format, optimize=True, quality=quality
    )

    original_name = Path(image_field.name).stem
    new_name = _get_image_filename(original_name, final_format)

    return ContentFile(buffer.getvalue(), name=new_name)


def compress_image(
    image_field: ImageField,
    quality=85,
    img_format: Literal["DEFAULT", "WEBP"] | str = "WEBP",
):
    """
    Compress an image to reduce file size. Returns a Django ContentFile ready
    to save to an ImageField.
    """
    img = Image.open(image_field)
    final_format = img.format if img_format == "DEFAULT" else img_format

    buffer = BytesIO()
    img.save(buffer, format=final_format, optimize=True, quality=quality)

    original_name = Path(image_field.name).stem
    new_name = _get_image_filename(original_name, final_format)
    return ContentFile(buffer.getvalue(), name=new_name)


def scale_and_compress(
    image_field: ImageField,
    max_width=800,
    max_height=800,
    quality=85,
    img_format: Literal["DEFAULT", "WEBP"] | str = "WEBP",
):
    """
    Resize and compress an image in one step. Returns a Django ContentFile
    ready to save to an ImageField.
    """
    img = Image.open(image_field)
    final_format = img.format if img_format == "DEFAULT" else img_format

    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

    buffer = BytesIO()
    img.save(buffer, format=final_format, optimize=True, quality=quality)

    original_name = Path(image_field.name).stem
    new_name = _get_image_filename(original_name, final_format)
    return ContentFile(buffer.getvalue(), name=new_name)


def convert_to_webp(image_field: ImageField, quality: int = 85):
    return compress_image(image_field, quality)


class DumpableModelMixin(models.Model):
    """
    Adds `.model_dump(relations=None, all=False, exclude=None)`.

    - relations: list of Django-style paths ("author", "author__awards").
    - exclude: list of paths to skip.
    - all=False → expand only listed relations.
    - all=True  → expand all relations recursively, unless excluded.
    - Prevents repeating objects: already visited collapse to {pk_name: value}.
    - FileField / ImageField → dumps `.url` if available, else None.
    - JSONField → ensures valid JSON-serializable structure.
    - Date/DateTime/Time → ISO8601 strings.
    - DecimalField → string.
    - If related object lacks `.model_dump`, warns and returns only PK.
    """

    class Meta:
        abstract = True

    def model_dump(
        self,
        relations: list[RelationPath] | None = None,
        all: bool = False,
        exclude: list[RelationPath] | None = None,
        _visited: set[tuple[str, any]] | None = None,
        _is_root: bool = True,
    ) -> dict[str, any]:
        relations = relations or []
        exclude = exclude or []

        rel_map = _build_rel_map(relations)
        exclude_map = _build_rel_map(exclude)

        if _visited is None:
            _visited = set()

        model_key = (
            self._meta.label,
            getattr(self, self._meta.pk.attname, None),
        )
        if model_key in _visited and not _is_root:
            return {self._meta.pk.name: getattr(self, self._meta.pk.attname)}

        _visited.add(model_key)
        payload: dict[str, any] = {}

        for field in self._meta.get_fields():
            name = field.name
            is_relation = field.is_relation

            if name in exclude_map and not exclude_map[name]:
                continue

            nested_exclude = exclude_map.get(name, {})
            nested_rel = rel_map.get(name, {})

            expand = False
            if name in nested_rel:
                expand = True
            elif all and is_relation and name not in exclude_map:
                expand = True

            if getattr(field, "concrete", False):
                if isinstance(field, (ForeignKey, OneToOneField)):
                    if field.name in exclude or all is False:
                        continue

                    related_obj = getattr(self, name, None)
                    if related_obj is None:
                        payload[name] = None
                    elif expand:
                        if hasattr(related_obj, "model_dump"):
                            payload[name] = related_obj.model_dump(
                                relations=_flatten_rel_map(nested_rel),
                                exclude=_flatten_rel_map(nested_exclude),
                                all=all,
                                _visited=_visited,
                                _is_root=False,
                            )
                        else:
                            warnings.warn(
                                f"{related_obj.__class__.__name__} has no model_dump; "  # noqa: E501
                                "returning only {field.attname}"
                            )
                            payload[name] = getattr(self, field.attname)
                    else:
                        payload[name] = getattr(self, field.attname)

                elif isinstance(field, (models.FileField, models.ImageField)):
                    file_obj = getattr(self, name, None)
                    payload[name] = (
                        file_obj.url
                        if (file_obj and getattr(file_obj, "url", None))
                        else None
                    )

                elif isinstance(field, models.JSONField):
                    value = getattr(self, name, None)
                    if value is None:
                        payload[name] = None
                    elif isinstance(value, (dict, list, str, int, float, bool)):
                        payload[name] = value
                    else:
                        payload[name] = str(value)

                elif isinstance(
                    field,
                    (models.DateTimeField, models.DateField, models.TimeField),
                ):
                    value = getattr(self, name, None)
                    payload[name] = value.isoformat() if value else None

                elif isinstance(field, models.DecimalField):
                    value = getattr(self, field.attname)
                    payload[name] = str(value) if value is not None else None

                else:
                    payload[name] = getattr(self, field.attname)

            else:
                if not expand:
                    continue

                try:
                    attr = getattr(self, name)
                except Exception:
                    payload[name] = None
                    continue

                if hasattr(attr, "all"):
                    qs = attr.all()
                    payload[name] = []
                    for obj in qs:
                        if hasattr(obj, "model_dump"):
                            payload[name].append(
                                obj.model_dump(
                                    relations=_flatten_rel_map(nested_rel),
                                    exclude=_flatten_rel_map(nested_exclude),
                                    all=all,
                                    _visited=_visited,
                                    _is_root=False,
                                )
                            )
                        else:
                            warnings.warn(
                                f"{obj.__class__.__name__} has no model_dump; "
                                "returning only pk"
                            )
                            payload[name].append(
                                {
                                    obj._meta.pk.name: getattr(
                                        obj, obj._meta.pk.attname
                                    )
                                }
                            )
                else:
                    related_obj = attr
                    if related_obj is None:
                        payload[name] = None
                    elif hasattr(related_obj, "model_dump"):
                        payload[name] = related_obj.model_dump(
                            relations=_flatten_rel_map(nested_rel),
                            exclude=_flatten_rel_map(nested_exclude),
                            all=all,
                            _visited=_visited,
                            _is_root=False,
                        )
                    else:
                        warnings.warn(
                            f"{related_obj.__class__.__name__} has no model"
                            " dump; returning only pk"
                        )
                        payload[name] = {
                            related_obj._meta.pk.name: getattr(
                                related_obj, related_obj._meta.pk.attname
                            )
                        }

        if _is_root:
            _visited.clear()
        return payload


def _build_rel_map(paths: list[str]) -> dict[str, any]:
    rel_map: dict[str, any] = {}
    for path in paths:
        parts = path.split("__")
        current = rel_map
        for part in parts:
            current = current.setdefault(part, {})
    return rel_map


def _flatten_rel_map(rel_map: dict[str, any], prefix: str = "") -> list[str]:
    paths = []
    for k, v in rel_map.items():
        new_prefix = f"{prefix}__{k}" if prefix else k
        paths.append(new_prefix)
        if v:
            paths.extend(_flatten_rel_map(v, new_prefix))
    return paths


class ModelCloudFileSupport(models.Model):
    class Meta:
        abstract = True

    def upload_to_cloud(self):
        # Call this from .save() or from signal
        for field_name in self.tracker.fields:
            if not self.tracker.has_changed(field_name):
                continue

            file_field = getattr(self, field_name)
            if not file_field:
                continue

            file_url = cloud_storage.upload_sync(file_field)
            if file_url:
                setattr(self, f"{field_name}_cloud_url", file_url)

    def model_dump_with_cloud_url(self, dumped: dict) -> dict:
        for field_name in self.tracker.fields:
            dumped[field_name] = cloud_storage.get_best_file_url(
                local_file=getattr(self, field_name),
                cloud_url=getattr(self, f"{field_name}_cloud_url"),
            )

        return dumped


class DumpableModelCloudFileSupport(DumpableModelMixin, ModelCloudFileSupport):
    """Inherits both `DumpableModelMixin` and `ModelCloudFileSupport`"""

    class Meta:
        abstract = True
