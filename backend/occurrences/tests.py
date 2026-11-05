from django.test import TestCase


class OccurrenceAppTests(TestCase):
    def test_admin_route_exists(self):
        response = self.client.get("/admin/login/")

        self.assertEqual(response.status_code, 200)
