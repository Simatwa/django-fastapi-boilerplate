from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.forms import ImportForm, SelectableFieldsExportForm

from project import settings


class CustomImportExportModelAdmin(ImportExportModelAdmin):
    """ImportExportModelAdmin;`ImportForm` and `SelectableFieldsExportForm`"""

    import_class_form = ImportForm
    export_class_form = SelectableFieldsExportForm


DevelopmentImportExportModelAdmin = (
    CustomImportExportModelAdmin if settings.DEBUG else admin.ModelAdmin
)
"""ModelAdmin for importing & exporting entries in `development environment`"""
