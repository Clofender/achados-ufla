from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import FileExtensionValidator


class Profile(models.Model):
    class Role(models.TextChoices):
        STUDENT = "student", "Estudante"
        MODERATOR = "moderator", "Moderador"
        ADMIN = "admin", "Administrador"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    phone = models.CharField("telefone", max_length=30, blank=True)
    campus_id = models.CharField("matrícula", max_length=40, blank=True)
    role = models.CharField("perfil", max_length=20, choices=Role.choices, default=Role.STUDENT)
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        verbose_name = "perfil"
        verbose_name_plural = "perfis"

    def __str__(self):
        return f"Perfil de {self.user.get_username()}"


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
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="proprietário",
        null=True,
        blank=True,
    )
    image = models.FileField(
        "foto",
        upload_to="items/%Y/%m/",
        blank=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"])],
    )
    contact_note = models.CharField("observação de contato", max_length=255, blank=True)
    is_public = models.BooleanField("público", default=True)
    approved = models.BooleanField("aprovado", default=False)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="approved_items",
        null=True,
        blank=True,
        verbose_name="aprovado por",
    )
    approved_at = models.DateTimeField("aprovado em", null=True, blank=True)
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
        if self.image and self.image.size > 5 * 1024 * 1024:
            raise ValidationError({"image": "A foto deve ter no máximo 5 MB."})

    def __str__(self):
        return self.title
