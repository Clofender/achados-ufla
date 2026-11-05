from django.core.exceptions import ValidationError
from django.db import models


class Category(models.Model):
    name = models.CharField("nome", max_length=80, unique=True)
    description = models.TextField("descrição", blank=True)
    is_active = models.BooleanField("ativa", default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "categoria"
        verbose_name_plural = "categorias"

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField("nome", max_length=120, unique=True)
    description = models.TextField("descrição", blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "local"
        verbose_name_plural = "locais"

    def __str__(self):
        return self.name


class Item(models.Model):
    class Status(models.TextChoices):
        LOST = "LOST", "Perdido"
        FOUND = "FOUND", "Encontrado"
        RETURNED = "RETURNED", "Devolvido"
        ARCHIVED = "ARCHIVED", "Arquivado"

    title = models.CharField("título", max_length=160)
    description = models.TextField("descrição")
    characteristics = models.TextField("características", blank=True)
    status = models.CharField(
        "status",
        max_length=10,
        choices=Status.choices,
        default=Status.LOST,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="items",
        verbose_name="categoria",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="items",
        verbose_name="local relacionado",
    )
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "objeto"
        verbose_name_plural = "objetos"
        indexes = [
            models.Index(fields=["status", "-created_at"]),
        ]

    def clean(self):
        if self.status == self.Status.RETURNED and not self.characteristics.strip():
            raise ValidationError(
                {"characteristics": "Objetos devolvidos devem ter características registradas."}
            )

    def __str__(self):
        return self.title
