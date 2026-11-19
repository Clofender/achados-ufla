from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.utils import timezone

from core.models import Category, Item, Location, Profile
from occurrences.models import Occurrence


class Command(BaseCommand):
    help = "Cria dados públicos de demonstração do Achados UFLA."

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            help="Usuário existente que será usado como responsável pelos registros.",
        )

    def handle(self, *args, **options):
        user_model = get_user_model()
        username = options.get("username") or "demo_aluno"
        reporter, created = user_model.objects.get_or_create(
            username=username,
            defaults={
                "first_name": "Estudante",
                "last_name": "Demo",
                "email": f"{username}@example.local",
            },
        )
        if created:
            reporter.set_password("Demo12345!")
            reporter.save(update_fields=["password"])
        Profile.objects.filter(user=reporter).update(role=Profile.Role.STUDENT)

        moderator, moderator_created = user_model.objects.get_or_create(
            username="demo_moderador",
            defaults={"email": "demo_moderador@example.local"},
        )
        if moderator_created:
            moderator.set_password("Demo12345!")
            moderator.save(update_fields=["password"])
        moderator.is_staff = True
        moderator.save(update_fields=["is_staff"])
        Profile.objects.filter(user=moderator).update(role=Profile.Role.MODERATOR)
        moderator.user_permissions.add(
            Permission.objects.get(codename="change_occurrence", content_type__app_label="occurrences")
        )

        administrator, administrator_created = user_model.objects.get_or_create(
            username="demo_admin",
            defaults={"email": "demo_admin@example.local"},
        )
        if administrator_created:
            administrator.set_password("Demo12345!")
            administrator.save(update_fields=["password"])
        administrator.is_staff = True
        administrator.is_superuser = True
        administrator.save(update_fields=["is_staff", "is_superuser"])
        Profile.objects.filter(user=administrator).update(role=Profile.Role.ADMIN)

        electronics, _ = Category.objects.get_or_create(
            name="Eletrônicos",
            defaults={"description": "Celulares, notebooks e acessórios."},
        )
        documents, _ = Category.objects.get_or_create(
            name="Documentos",
            defaults={"description": "Documentos e cartões encontrados."},
        )
        library, _ = Location.objects.get_or_create(
            name="Biblioteca Universitária",
            defaults={"description": "Prédio central da biblioteca."},
        )
        restaurant, _ = Location.objects.get_or_create(
            name="Restaurante Universitário",
            defaults={"description": "Área de atendimento do restaurante."},
        )

        phone, _ = Item.objects.get_or_create(
            title="Celular preto",
            defaults={
                "description": "Celular encontrado próximo à entrada.",
                "characteristics": "Capa azul e pequeno risco na lateral.",
                "status": Item.Status.FOUND,
                "category": electronics,
                "location": library,
                "owner": reporter,
                "approved": True,
                "approved_by": moderator,
                "approved_at": timezone.now(),
            },
        )
        card, _ = Item.objects.get_or_create(
            title="Cartão estudantil",
            defaults={
                "description": "Cartão estudantil encontrado em uma mesa.",
                "characteristics": "Nome parcialmente coberto por proteção.",
                "status": Item.Status.LOST,
                "category": documents,
                "location": restaurant,
                "owner": reporter,
            },
        )

        Occurrence.objects.get_or_create(
            item=phone,
            occurrence_type=Occurrence.Type.FINDING,
            reporter=reporter,
            location=library,
            defaults={
                "occurred_at": timezone.now(),
                "notes": "Entregue na recepção da biblioteca.",
            },
        )
        Occurrence.objects.get_or_create(
            item=card,
            occurrence_type=Occurrence.Type.LOSS,
            reporter=reporter,
            location=restaurant,
            defaults={
                "occurred_at": timezone.now(),
                "notes": "Último local informado pelo estudante.",
            },
        )

        self.stdout.write(self.style.SUCCESS("Dados de demonstração criados."))
