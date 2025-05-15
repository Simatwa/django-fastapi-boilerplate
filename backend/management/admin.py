from django.contrib import admin
from management.models import (
    MemberGroup,
    GroupMessage,
    PersonalMessage,
    Concern,
    AppUtility,
)
from project.utils.admin import DevelopmentImportExportModelAdmin
from django.utils.translation import gettext_lazy as _
from management.forms import AppUtilityForm


# Register your models here.
@admin.register(MemberGroup)
class MemberGroupAdmin(DevelopmentImportExportModelAdmin):
    list_display = ("name", "description", "social_media_link")
    search_fields = ("name", "description", "members__username")
    filter_horizontal = ("members",)
    fieldsets = (
        (
            None,
            {
                "fields": ("name", "description", "members"),
                "classes": ["tab"],
            },
        ),
        (
            _("Social Forum Link"),
            {
                "fields": ("social_media_link",),
                "classes": ["tab"],
            },
        ),
    )


@admin.register(GroupMessage)
class GroupMessageAdmin(DevelopmentImportExportModelAdmin):
    list_display = ("subject", "category", "created_at", "updated_at")
    search_fields = ("subject", "category", "groups__name")
    list_filter = ("category", "groups", "created_at", "updated_at")
    filter_horizontal = ("groups",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "category",
                    "groups",
                ),
                "classes": ["tab"],
            },
        ),
        (
            _("Message"),
            {
                "fields": ("subject", "content"),
                "classes": ["tab"],
            },
        ),
        (
            _("Timestamps"),
            {"fields": ("created_at", "updated_at"), "classes": ["tab"]},
        ),
    )
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)


@admin.register(PersonalMessage)
class PersonalMessageAdmin(DevelopmentImportExportModelAdmin):
    list_display = (
        "user",
        "category",
        "subject",
        "is_read",
        "created_at",
        "updated_at",
    )
    search_fields = ("user__username", "subject", "content", "category")
    list_filter = ("category", "is_read", "created_at", "updated_at")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "category",
                ),
                "classes": ["tab"],
            },
        ),
        (
            _("Message"),
            {
                "fields": (
                    "subject",
                    "content",
                ),
                "classes": ["tab"],
            },
        ),
        (
            _("Read Status & Timestamps"),
            {"fields": ("is_read", "created_at", "updated_at"), "classes": ["tab"]},
        ),
    )
    readonly_fields = ("created_at", "updated_at", "is_read")
    ordering = ("-created_at",)


@admin.register(Concern)
class ConcernAdmin(DevelopmentImportExportModelAdmin):
    list_display = ("user", "about", "status", "updated_at", "created_at")
    list_editable_fields = ("status",)
    search_fields = ("user__username", "about", "details", "response", "status")
    list_filter = ("status", "updated_at", "created_at")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "about",
                    "details",
                ),
                "classes": ["tab"],
            },
        ),
        (
            _("Response & Status"),
            {
                "fields": (
                    "status",
                    "response",
                ),
                "classes": ["tab"],
            },
        ),
        (
            _("Timestamps"),
            {"fields": ("created_at", "updated_at"), "classes": ["tab"]},
        ),
    )
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-updated_at",)


@admin.register(AppUtility)
class AppUtilityAdmin(DevelopmentImportExportModelAdmin):
    form = AppUtilityForm
    list_display = ("name", "value", "updated_at", "created_at")
    search_fields = ("name", "details")
    ordering = ("-updated_at",)
    fieldsets = (
        (None, {"fields": ("name", "description", "value")}),
        (_("Timestamps"), {"fields": ("updated_at", "created_at")}),
    )
    readonly_fields = ("updated_at", "created_at")
