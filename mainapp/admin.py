from django.contrib import admin
from .models import History


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = (
        "request_id",
        "task_type",
        "predictions",
        "version_code",
        "status",
        "created",
    )
    search_fields = ("request_id", "predictions")
    list_filter = ("task_type", "status", "version_code")
    readonly_fields = ("created",)
