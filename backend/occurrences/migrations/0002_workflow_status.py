import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("occurrences", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="occurrence",
            name="occurrence_type",
            field=models.CharField(choices=[("LOSS", "Perda"), ("FINDING", "Achado"), ("RETURN_REQUEST", "Solicitação de devolução")], max_length=16, verbose_name="tipo"),
        ),
        migrations.AddField(
            model_name="occurrence", name="status",
            field=models.CharField(choices=[("PENDING", "Pendente"), ("APPROVED", "Aprovada"), ("REJECTED", "Rejeitada"), ("COMPLETED", "Concluída")], default="PENDING", max_length=10, verbose_name="status"),
        ),
        migrations.AddField(
            model_name="occurrence", name="reviewed_by",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="reviewed_occurrences", to=settings.AUTH_USER_MODEL, verbose_name="revisado por"),
        ),
        migrations.AddField(
            model_name="occurrence", name="reviewed_at",
            field=models.DateTimeField(blank=True, null=True, verbose_name="revisado em"),
        ),
    ]
