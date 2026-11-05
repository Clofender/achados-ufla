from django.contrib import admin

from .models import Category, Item, Location


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "location", "status", "created_at")
    search_fields = ("title", "description", "characteristics")
    readonly_fields = ("created_at", "updated_at")
