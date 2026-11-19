import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("occurrences", "0002_workflow_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="occurrence",
            name="return_notes",
            field=models.TextField(blank=True, verbose_name="observação da devolução"),
        ),
        migrations.AddField(
            model_name="occurrence",
            name="returned_to",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="received_items",
                to=settings.AUTH_USER_MODEL,
                verbose_name="devolvido para",
            ),
        ),
    ]
