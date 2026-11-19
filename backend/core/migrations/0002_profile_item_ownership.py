import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("phone", models.CharField(blank=True, max_length=30, verbose_name="telefone")),
                ("campus_id", models.CharField(blank=True, max_length=40, verbose_name="matrícula")),
                ("role", models.CharField(choices=[("student", "Estudante"), ("moderator", "Moderador"), ("admin", "Administrador")], default="student", max_length=20, verbose_name="perfil")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="criado em")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="atualizado em")),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="profile", to=settings.AUTH_USER_MODEL)),
            ],
            options={"verbose_name": "perfil", "verbose_name_plural": "perfis"},
        ),
        migrations.AddField(
            model_name="item", name="approved",
            field=models.BooleanField(default=False, verbose_name="aprovado"),
        ),
        migrations.AddField(
            model_name="item", name="approved_at",
            field=models.DateTimeField(blank=True, null=True, verbose_name="aprovado em"),
        ),
        migrations.AddField(
            model_name="item", name="contact_note",
            field=models.CharField(blank=True, max_length=255, verbose_name="observação de contato"),
        ),
        migrations.AddField(
            model_name="item", name="image",
            field=models.FileField(blank=True, upload_to="items/%Y/%m/", validators=[django.core.validators.FileExtensionValidator(["jpg", "jpeg", "png", "webp"])], verbose_name="foto"),
        ),
        migrations.AddField(
            model_name="item", name="is_public",
            field=models.BooleanField(default=True, verbose_name="público"),
        ),
        migrations.AddField(
            model_name="item", name="owner",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="items", to=settings.AUTH_USER_MODEL, verbose_name="proprietário"),
        ),
        migrations.AddField(
            model_name="item", name="approved_by",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="approved_items", to=settings.AUTH_USER_MODEL, verbose_name="aprovado por"),
        ),
    ]
