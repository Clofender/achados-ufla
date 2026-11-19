from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from core.models import Category, Item, Location, Profile

from .models import Occurrence

class OccurrenceAppTests(TestCase):
    def test_admin_route_exists(self):
        response = self.client.get("/admin/login/")

        self.assertEqual(response.status_code, 200)

    def setUp(self):
        self.user = get_user_model().objects.create_user(username="aluno", password="Senha12345!")
        self.moderator = get_user_model().objects.create_user(
            username="moderador", password="Senha12345!"
        )
        self.moderator.profile.role = Profile.Role.MODERATOR
        self.moderator.profile.save()
        self.category = Category.objects.create(name="Acessórios")
        self.location = Location.objects.create(name="Pavilhão")
        self.item = Item.objects.create(
            title="Chaves",
            description="Chaves encontradas.",
            category=self.category,
            location=self.location,
            owner=self.user,
            status=Item.Status.FOUND,
        )

    def test_occurrence_starts_pending_and_is_owned_by_reporter(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("occurrences:create"),
            {
                "item": self.item.pk,
                "occurrence_type": Occurrence.Type.RETURN_REQUEST,
                "location": self.location.pk,
                "occurred_at": timezone.now().strftime("%Y-%m-%dT%H:%M"),
                "notes": "Tenho a identificação do objeto.",
            },
        )
        self.assertEqual(response.status_code, 302)
        occurrence = Occurrence.objects.get()
        self.assertEqual(occurrence.reporter, self.user)
        self.assertEqual(occurrence.status, Occurrence.Status.PENDING)

    def test_moderator_approval_returns_item_atomically(self):
        occurrence = Occurrence.objects.create(
            item=self.item,
            occurrence_type=Occurrence.Type.RETURN_REQUEST,
            reporter=self.user,
            location=self.location,
            occurred_at=timezone.now(),
        )
        self.client.force_login(self.moderator)
        response = self.client.post(reverse("occurrences:approve_return", args=[occurrence.pk]))
        self.assertEqual(response.status_code, 302)
        occurrence.refresh_from_db()
        self.item.refresh_from_db()
        self.assertEqual(occurrence.status, Occurrence.Status.APPROVED)
        self.assertEqual(occurrence.reviewed_by, self.moderator)
        self.assertEqual(self.item.status, Item.Status.RETURNED)
