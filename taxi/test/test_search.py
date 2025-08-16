from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test", password="test123"
        )
        self.client.login(username="test", password="test123")

        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Tesla", country="USA")
        Manufacturer.objects.create(name="Ford", country="USA")

    def test_search_contains(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-list"),
            {"name": "Tesla"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tesla")

    def test_search_icontains(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-list"),
            {"name": "tes"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tesla")

    def test_search_with_out_arguments(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-list"),
            {"name": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Tesla")
        self.assertContains(response, "Ford")
