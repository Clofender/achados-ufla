from django.contrib import admin

from .models import Occurrence


@admin.register(Occurrence)
class OccurrenceAdmin(admin.ModelAdmin):
    list_display = (
        "item",
        "occurrence_type",
        "location",
        "reporter",
        "occurred_at",
    )
    search_fields = ("item__title", "location__name", "reporter__username")
    readonly_fields = ("created_at",)
