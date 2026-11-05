from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from core.models import Item, Location


class Occurrence(models.Model):
    class Type(models.TextChoices):
        LOSS = "LOSS", "Perda"
        FINDING = "FINDING", "Achado"

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="occurrences",
        verbose_name="objeto",
    )
    occurrence_type = models.CharField(
        "tipo",
        max_length=7,
        choices=Type.choices,
    )
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="reported_occurrences",
        verbose_name="responsável pelo registro",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="occurrences",
        verbose_name="local",
    )
    occurred_at = models.DateTimeField("data e hora da ocorrência")
    notes = models.TextField("observações", blank=True)
    created_at = models.DateTimeField("registrado em", auto_now_add=True)

    class Meta:
        ordering = ["-occurred_at"]
        verbose_name = "ocorrência"
        verbose_name_plural = "ocorrências"
        indexes = [
            models.Index(fields=["occurrence_type", "-occurred_at"]),
        ]

    def clean(self):
        if self.occurred_at > timezone.now():
            raise ValidationError(
                {"occurred_at": "A data da ocorrência não pode estar no futuro."}
            )

    def __str__(self):
        return f"{self.get_occurrence_type_display()} — {self.item}"
