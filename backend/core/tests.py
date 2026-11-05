from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from occurrences.models import Occurrence

from .models import Category, Item, Location


class DomainModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Eletrônicos")
        self.location = Location.objects.create(name="Biblioteca")
        self.user = get_user_model().objects.create_user(
            username="responsavel",
            password="senha-segura",
        )

    def test_item_has_related_category_and_location(self):
        item = Item.objects.create(
            title="Notebook",
            description="Notebook encontrado.",
            category=self.category,
            location=self.location,
        )

        self.assertEqual(item.category.name, "Eletrônicos")
        self.assertEqual(item.location.name, "Biblioteca")
        self.assertEqual(str(item), "Notebook")

    def test_returned_item_requires_characteristics(self):
        item = Item(
            title="Chaves",
            description="Chaves devolvidas.",
            status=Item.Status.RETURNED,
            category=self.category,
            location=self.location,
        )

        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_occurrence_cannot_be_in_the_future(self):
        occurrence = Occurrence(
            item=Item.objects.create(
                title="Carteira",
                description="Carteira encontrada.",
                category=self.category,
                location=self.location,
            ),
            occurrence_type=Occurrence.Type.FINDING,
            reporter=self.user,
            location=self.location,
            occurred_at=timezone.now() + timedelta(days=1),
        )

        with self.assertRaises(ValidationError):
            occurrence.full_clean()
