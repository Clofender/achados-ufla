from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.utils import timezone

from core.models import Category, Item, Location
from occurrences.models import Occurrence


class Command(BaseCommand):
    help = "Cria dados públicos de demonstração do Achados UFLA."

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            required=True,
            help="Usuário existente que será usado como responsável pelos registros.",
        )

    def handle(self, *args, **options):
        username = options["username"]
        user_model = get_user_model()
        try:
            reporter = user_model.objects.get(username=username)
        except user_model.DoesNotExist as exc:
            raise CommandError(
                f"O usuário '{username}' não existe. Crie-o antes com createsuperuser."
            ) from exc

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
