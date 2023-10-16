from urllib.parse import urlencode

from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from core.models import Budget, Category, FinancialEntry


@override_settings(MEDIA_ROOT="TEST_DIR")
class TestSimpleHTTPMethodsFinancialEntriesView(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username="test", password="test", email="test@tivix.com"
        )
        cls.user.save()
        Budget.objects.create(user=cls.user, name="test").save()
        Category.objects.create(
            user=cls.user, name="test", budget=Budget.objects.get(name="test")
        ).save()
        FinancialEntry.objects.create(
            user=cls.user,
            description="test",
            amount=100,
            entry_type="EXPENSE",
            date="2021-01-01",
            category=Category.objects.get(name="test"),
        ).save()
        cls.client = APIClient()

    @classmethod
    def tearDownClass(cls) -> None:
        User.objects.all().delete()
        Budget.objects.all().delete()
        Category.objects.all().delete()
        return super().tearDownClass()

    def test_list_financial_entries_unauthenticated(self):
        response = self.client.get(reverse("financial-entries-list"))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "Authentication credentials were not provided."},
        )

    def test_list_financial_entries_authenticated(self):
        self.client.login(username="test", password="test")
        response = self.client.get(reverse("financial-entries-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 1,
                        "url": "http://testserver/financial-entries/1/",
                        "category": "http://testserver/categories/1/",
                        "amount": "100.00",
                        "description": "test",
                        "date": response.json()["results"][0]["date"],
                        "entry_type": "EXPENSE",
                        "user": 1,
                    },
                ],
            },
        )

    def test_get_financial_entry_unauthenticated(self):
        response = self.client.get(reverse("financial-entries-detail", args=[1]))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "Authentication credentials were not provided."},
        )

    def test_get_financial_entry_authenticated(self):
        self.client.login(username="test", password="test")
        response = self.client.get(reverse("financial-entries-detail", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "id": 1,
                "url": "http://testserver/financial-entries/1/",
                "category": "http://testserver/categories/1/",
                "amount": "100.00",
                "description": "test",
                "date": response.json()["date"],
                "entry_type": "EXPENSE",
                "user": 1,
            },
        )
