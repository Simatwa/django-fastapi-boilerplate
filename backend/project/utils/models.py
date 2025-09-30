import warnings
from io import BytesIO

from django.core.files.base import ContentFile
from django.db import models
from django.db.models.fields.related import ForeignKey, OneToOneField
from PIL import Image

RelationPath = str  # "__"-style


def resize_image(image_field, max_width=800, max_height=800):
    """
    Resize an image to fit within max_width and max_height while maintaining
    aspect ratio.
    Returns a Django ContentFile ready to save to an ImageField.

    ## Usage example

    ```python
    model_instance.image=resize_image(model_instance.image)
    ```
    """
    img = Image.open(image_field)
    img_format = img.format or "JPEG"

    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

    buffer = BytesIO()
    img.save(buffer, format=img_format, optimize=True, quality=85)
    return ContentFile(buffer.getvalue(), name=image_field.name)


def compress_image(image_field, quality=70):
    """
    Compress an image to reduce file size.
    Returns a Django ContentFile ready to save to an ImageField.
    ## Usage example

    ```python
    model_instance.image=compress_image(model_instance.image)
    ```
    """
    img = Image.open(image_field)
    img_format = img.format or "JPEG"

    buffer = BytesIO()
    img.save(buffer, format=img_format, optimize=True, quality=quality)
    return ContentFile(buffer.getvalue(), name=image_field.name)


def scale_and_compress(image_field, max_width=800, max_height=800, quality=75):
    """
    Resize and compress an image in one step.

    ## Usage example

    ```python
    model_instance.image=scale_and_resize(model_instance.image)
    ```
    """
    img = Image.open(image_field)
    img_format = img.format or "JPEG"

    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

    buffer = BytesIO()
    img.save(buffer, format=img_format, optimize=True, quality=quality)
    return ContentFile(buffer.getvalue(), name=image_field.name)


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
