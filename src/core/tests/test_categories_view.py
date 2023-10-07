from urllib.parse import urlencode

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from core.models import Budget, Category


@override_settings(MEDIA_ROOT="TEST_DIR")
class TestListCategoriesView(TestCase):
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
        cls.client = APIClient()

    @classmethod
    def tearDownClass(cls) -> None:
        User.objects.all().delete()
        Budget.objects.all().delete()
        Category.objects.all().delete()
        return super().tearDownClass()

    def test_list_categories_unauthenticated(self):
        response = self.client.get("/categories/")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "Authentication credentials were not provided."},
        )

    def test_list_categories_authenticated(self):
        self.client.login(username="test", password="test")
        response = self.client.get("/categories/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "budget": "http://testserver/budgets/1/",
                        "name": "test",
                        "financial_entries": [],
                        "bilance": 0,
                        "url": "http://testserver/categories/1/",
                    },
                ],
            },
            response.json(),
        )


@override_settings(MEDIA_ROOT="TEST_DIR")
class TestSimpleHTTPMethodsCategoriesView(TestCase):
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
        cls.client = APIClient()

    @classmethod
    def tearDownClass(cls) -> None:
        User.objects.all().delete()
        Budget.objects.all().delete()
        Category.objects.all().delete()
        return super().tearDownClass()

    def test_post_categories_unauthenticated(self):
        response = self.client.post("/categories/", {"name": "test", "budget": 1})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "Authentication credentials were not provided."},
        )

    def test_post_categories_authenticated(self):
        self.client.login(username="test", password="test")
        response = self.client.post(
            "/categories/",
            {"name": "test", "budget": "http://testserver/budgets/1/"},
            content_type="application/json",
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {
                "budget": "http://testserver/budgets/1/",
                "name": "test",
                "financial_entries": [],
                "bilance": 0,
                "url": "http://testserver/categories/2/",
            },
            response.json(),
        )

    def test_put_categories_unauthenticated(self):
        response = self.client.put("/categories/1/", {"name": "test", "budget": 1})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "Authentication credentials were not provided."},
        )

    def test_put_categories_authenticated(self):
        self.client.login(username="test", password="test")
        response = self.client.put(
            "/categories/1/",
            data=urlencode({"name": "test", "budget": "http://testserver/budgets/1/"}),
            content_type="application/x-www-form-urlencoded",  # https://github.com/jgorset/django-respite/issues/38
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "budget": "http://testserver/budgets/1/",
                "name": "test",
                "financial_entries": [],
                "bilance": 0,
                "url": "http://testserver/categories/1/",
            },
            response.json(),
        )

    def test_delete_categories_unauthenticated(self):
        response = self.client.delete("/categories/1/")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "Authentication credentials were not provided."},
        )

    def test_delete_categories_authenticated(self):
        self.client.login(username="test", password="test")
        response = self.client.delete("/categories/1/")
        self.assertEqual(response.status_code, 204)
