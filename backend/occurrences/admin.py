from django.contrib import admin
from django.contrib import messages
from django.db import transaction
from django.utils import timezone

from .models import Occurrence


@admin.register(Occurrence)
class OccurrenceAdmin(admin.ModelAdmin):
    @admin.action(description="Aprovar solicitações de devolução")
    def approve_returns(self, request, queryset):
        count = 0
        with transaction.atomic():
            for occurrence in queryset.select_related("item"):
                if occurrence.occurrence_type != Occurrence.Type.RETURN_REQUEST:
                    continue
                occurrence.status = Occurrence.Status.APPROVED
                occurrence.reviewed_by = request.user
                occurrence.reviewed_at = timezone.now()
                occurrence.returned_to = occurrence.reporter
                occurrence.return_notes = occurrence.notes
                occurrence.save(
                    update_fields=[
                        "status",
                        "reviewed_by",
                        "reviewed_at",
                        "returned_to",
                        "return_notes",
                    ]
                )
                occurrence.item.status = occurrence.item.Status.RETURNED
                occurrence.item.approved = True
                occurrence.item.approved_by = request.user
                occurrence.item.approved_at = timezone.now()
                occurrence.item.save(
                    update_fields=["status", "approved", "approved_by", "approved_at", "updated_at"]
                )
                count += 1
        self.message_user(request, f"{count} devolução(ões) aprovada(s).", messages.SUCCESS)

    @admin.action(description="Rejeitar ocorrências selecionadas")
    def reject_occurrences(self, request, queryset):
        updated = queryset.update(
            status=Occurrence.Status.REJECTED,
            reviewed_by=request.user,
            reviewed_at=timezone.now(),
        )
        self.message_user(request, f"{updated} ocorrência(s) rejeitada(s).", messages.SUCCESS)

    @admin.action(description="Marcar ocorrências como concluídas")
    def complete_occurrences(self, request, queryset):
        updated = queryset.update(
            status=Occurrence.Status.COMPLETED,
            reviewed_by=request.user,
            reviewed_at=timezone.now(),
        )
        self.message_user(request, f"{updated} ocorrência(s) concluída(s).", messages.SUCCESS)

    actions = ("approve_returns", "reject_occurrences", "complete_occurrences")
    list_display = (
        "item",
        "occurrence_type",
        "location",
        "reporter",
        "status",
        "occurred_at",
    )
    search_fields = ("item__title", "location__name", "reporter__username", "notes")
    list_filter = ("occurrence_type", "status", "location", "occurred_at")
    ordering = ("-occurred_at",)
    date_hierarchy = "occurred_at"
    list_select_related = ("item", "location", "reporter")
    autocomplete_fields = ("item", "location", "reporter")
    readonly_fields = ("created_at", "reviewed_by", "reviewed_at")
    fieldsets = (
        ("Registro", {"fields": ("item", "occurrence_type", "reporter")}),
        ("Quando e onde", {"fields": ("occurred_at", "location")}),
        ("Fluxo de validação", {"fields": ("status", "reviewed_by", "reviewed_at", "returned_to", "return_notes")}),
        ("Observações", {"fields": ("notes",)}),
        (
            "Data do cadastro",
            {"fields": ("created_at",), "classes": ("collapse",)},
        ),
    )
