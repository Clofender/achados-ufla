from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from occurrences.models import Occurrence

from .forms import RegisterForm
from .models import Category, Item, Location, Profile


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

    def test_user_creation_creates_profile(self):
        user = get_user_model().objects.create_user(
            username="novo",
            password="Senha12345!",
        )
        self.assertEqual(user.profile.role, Profile.Role.STUDENT)

    def test_registration_requires_unique_email(self):
        form = RegisterForm(
            data={
                "first_name": "Outra",
                "last_name": "Pessoa",
                "username": "outra",
                "email": self.user.email,
                "password1": "Senha12345!",
                "password2": "Senha12345!",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_anonymous_item_creation_redirects_to_login(self):
        response = self.client.get(reverse("items:create"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_item_owner_is_set_by_server(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("items:create"),
            {
                "title": "Mochila",
                "description": "Mochila azul.",
                "category": self.category.pk,
                "location": self.location.pk,
                "status": Item.Status.FOUND,
                "characteristics": "Um chaveiro.",
                "is_public": "on",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Item.objects.get(title="Mochila").owner, self.user)

    def test_owner_cannot_edit_another_users_item(self):
        other = get_user_model().objects.create_user(
            username="outro",
            password="Senha12345!",
        )
        item = Item.objects.create(
            title="Carteira",
            description="Carteira encontrada.",
            category=self.category,
            location=self.location,
            owner=other,
        )
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("items:edit", args=[item.pk]),
            {
                "title": "Alterada",
                "description": "Tentativa indevida.",
                "category": self.category.pk,
                "location": self.location.pk,
                "status": Item.Status.FOUND,
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_public_search_filters_by_title(self):
        Item.objects.create(
            title="Caderno verde",
            description="Anotações de aula.",
            category=self.category,
            location=self.location,
            owner=self.user,
            approved=True,
        )
        self.client.force_login(self.user)
        response = self.client.get(reverse("items:list"), {"q": "Caderno"})
        self.assertContains(response, "Caderno verde")
        self.assertNotContains(response, "Notebook")
