from urllib.parse import urlencode

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status

from core.factories.budget_factory import BudgetFactory
from core.factories.user_factory import UserFactory, DEFAULT_PASSWORD
from core.models import Budget, BudgetUser, User


@override_settings(MEDIA_ROOT="TEST_DIR")
class TestListBudgets(TestCase):
    def setUp(self):
        super().setUp()
        user = UserFactory()
        self.login = {
            "username": user.username,
            "password": DEFAULT_PASSWORD,
        }
        for i in range(10):
            BudgetFactory(
                user=user,
                name=f"test_{i+1}",
            )
        self.client = APIClient()

    def test_list_budgets_unauthorized(self):
        response = self.client.get(reverse("budgets-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_budgets_authorized(self):
        """Test list budgets for authorized user. Also check if shared budget is in response."""
        self.client.login(**self.login)
        response = self.client.get(reverse("budgets-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertEqual(len(results), 10)


@override_settings(MEDIA_ROOT="TEST_DIR")
class TestPostBudget(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username="test", password="test", email="test@tivix.com"
        )
        cls.user.save()
        cls.client = APIClient()

    @classmethod
    def tearDownClass(cls) -> None:
        User.objects.all().delete()
        Budget.objects.all().delete()
        return super().tearDownClass()

    def test_post_budget(self):
        self.client.login(username="test", password="test")
        response = self.client.post(
            reverse("budgets-list"), {"name": "test", "user": 1}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json(),
            {
                "user": 1,
                "owner": "test",
                "categories": [],
                "name": "test",
                "created_at": response.json()["created_at"],
                "shared_with_users": [],
                "url": "http://testserver/budgets/1/",
            },
        )

    def test_post_budget_bad_request_same_name(self):
        self.client.login(username="test", password="test")
        self.client.post(reverse("budgets-list"), {"name": "test", "user": 1})
        response = self.client.post(
            reverse("budgets-list"), {"name": "test", "user": 1}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"name": ["This field must be unique."]})

    def test_post_budget_bad_request_user_posting_on_others_user_budgets(self):
        User.objects.create_user(username="test2", password="test", email="test").save()
        self.client.login(username="test", password="test")
        response = self.client.post(
            reverse("budgets-list"), {"name": "test", "user": 2}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {"non_field_errors": ["This budget doesn't belong to you."]},
        )


@override_settings(MEDIA_ROOT="TEST_DIR")
class TestSimpleHTTPMethodsBudget(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username="test", password="test", email="tester@tivix.com"
        )
        cls.user.save()
        Budget.objects.create(user=cls.user, name="test").save()
        cls.client = APIClient()

    @classmethod
    def tearDownClass(cls) -> None:
        User.objects.all().delete()
        Budget.objects.all().delete()
        return super().tearDownClass()

    def test_get_budget_unauthorized(self):
        response = self.client.get(reverse("budgets-detail", args=[1]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json(),
            {"detail": "Authentication credentials were not provided."},
        )

    def test_get_budget_authorized(self):
        self.client.login(username="test", password="test")
        response = self.client.get(reverse("budgets-detail", args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "user": 1,
                "owner": "test",
                "categories": [],
                "name": "test",
                "created_at": response.json()["created_at"],
                "shared_with_users": [],
                "url": "http://testserver/budgets/1/",
            },
        )

    def test_put_budget_unauthorized(self):
        response = self.client.put(
            reverse("budgets-detail", args=[1]), {"name": "test"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json(),
            {"detail": "Authentication credentials were not provided."},
        )

    def test_put_budget_authorized(self):
        self.client.login(username="test", password="test")
        response = self.client.put(
            "/budgets/1/",
            data=urlencode(
                {"user": 1, "name": "test", "budget": "http://testserver/budgets/1/"}
            ),
            content_type="application/x-www-form-urlencoded",  # https://github.com/jgorset/django-respite/issues/38
            format="json",
        )
        b = Budget.objects.get(pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "user": 1,
                "owner": "test",
                "categories": [],
                "name": "test",
                "created_at": b.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "shared_with_users": [],
                "url": "http://testserver/budgets/1/",
            },
        )

    def test_delete_budget_unauthorized(self):
        response = self.client.delete(reverse("budgets-detail", args=[1]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json(),
            {"detail": "Authentication credentials were not provided."},
        )

    def test_delete_budget_authorized(self):
        self.client.login(username="test", password="test")
        response = self.client.delete(reverse("budgets-detail", args=[1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
