from django.contrib import admin
from django.contrib import messages
from django.utils import timezone

from .models import Category, Item, Location, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "campus_id", "phone", "updated_at")
    list_filter = ("role",)
    search_fields = ("user__username", "user__email", "campus_id")
    autocomplete_fields = ("user",)
    readonly_fields = ("created_at", "updated_at")


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
    @admin.action(description="Arquivar objetos selecionados")
    def archive_items(self, request, queryset):
        updated = queryset.exclude(status=Item.Status.RETURNED).update(
            status=Item.Status.ARCHIVED
        )
        self.message_user(request, f"{updated} objeto(s) arquivado(s).", messages.SUCCESS)

    @admin.action(description="Marcar objetos selecionados como devolvidos")
    def return_items(self, request, queryset):
        valid = queryset.exclude(characteristics="")
        updated = valid.update(
            status=Item.Status.RETURNED,
            approved=True,
            approved_by=request.user,
            approved_at=timezone.now(),
        )
        self.message_user(request, f"{updated} objeto(s) marcado(s) como devolvido(s).", messages.SUCCESS)

    actions = ("archive_items", "return_items")
    list_display = ("title", "status", "category", "location", "owner", "created_at")
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
    list_select_related = ("category", "location", "owner")
    autocomplete_fields = ("category", "location", "owner", "approved_by")
    readonly_fields = ("owner", "created_at", "updated_at", "approved_at")
    fieldsets = (
        ("Objeto", {"fields": ("title", "category", "description", "characteristics")}),
        ("Situação e localização", {"fields": ("status", "location", "is_public", "approved")}),
        ("Responsabilidade", {"fields": ("owner", "approved_by", "approved_at")}),
        (
            "Datas do cadastro",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
