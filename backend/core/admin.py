from django.contrib import admin

from .models import Category, Item, Location


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name", "description")
    list_filter = ("is_active",)
    ordering = ("name",)
    fields = ("name", "description", "is_active")


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description")
    ordering = ("name",)
    fields = ("name", "description")


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "location", "status", "created_at")
    search_fields = (
        "title",
        "description",
        "characteristics",
        "category__name",
        "location__name",
    )
    list_filter = ("status", "category", "location", "created_at")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    list_select_related = ("category", "location")
    autocomplete_fields = ("category", "location")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Objeto", {"fields": ("title", "category", "description", "characteristics")}),
        ("Situação e localização", {"fields": ("status", "location")}),
        (
            "Datas do cadastro",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
