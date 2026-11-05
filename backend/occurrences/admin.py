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
    search_fields = ("item__title", "location__name", "reporter__username", "notes")
    list_filter = ("occurrence_type", "location", "occurred_at")
    ordering = ("-occurred_at",)
    date_hierarchy = "occurred_at"
    list_select_related = ("item", "location", "reporter")
    autocomplete_fields = ("item", "location", "reporter")
    readonly_fields = ("created_at",)
    fieldsets = (
        ("Registro", {"fields": ("item", "occurrence_type", "reporter")}),
        ("Quando e onde", {"fields": ("occurred_at", "location")}),
        ("Observações", {"fields": ("notes",)}),
        (
            "Data do cadastro",
            {"fields": ("created_at",), "classes": ("collapse",)},
        ),
    )
