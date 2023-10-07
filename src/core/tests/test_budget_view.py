from urllib.parse import urlencode

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from core.models import Budget, BudgetUser


@override_settings(MEDIA_ROOT="TEST_DIR")
class TestListBudgets(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username="test", password="test", email="test@tivix.com"
        )
        cls.user.save()
        cls.budget1 = Budget.objects.create(name="test", user=cls.user)
        cls.budget1.save()
        user = User.objects.create_user(username="test2", password="test", email="test")
        user.save()
        cls.budget2 = Budget.objects.create(name="shared", user=user)
        cls.budget2.save()
        budget_user = BudgetUser.objects.create(
            owner=user, visitor=cls.user, budget=cls.budget2
        )
        budget_user.save()
        cls.client = APIClient()

    @classmethod
    def tearDownClass(cls) -> None:
        User.objects.all().delete()
        Budget.objects.all().delete()
        return super().tearDownClass()

    def test_list_budgets_unauthorized(self):
        response = self.client.get("/budgets/")
        self.assertEqual(response.status_code, 403)

    def test_list_budgets_authorized(self):
        """Test list budgets for authorized user. Also check if sharded budget is in response."""
        self.client.login(username="test", password="test")
        response = self.client.get("/budgets/")
        created_at1 = self.budget1.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        created_at2 = self.budget2.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        self.assertEqual(response.status_code, 200)
        self.maxDiff = None
        self.assertEqual(
            {
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "categories": [],
                        "name": "test",
                        "created_at": created_at1,
                        "shared_with_users": [],
                        "url": "http://testserver/budgets/1/",
                        "user": 1,
                        "owner": "test",
                    },
                    {
                        "categories": [],
                        "name": "shared",
                        "created_at": created_at2,
                        "shared_with_users": [
                            {
                                "visitor": "http://testserver/users/1/",
                            }
                        ],
                        "url": "http://testserver/budgets/2/",
                        "user": 2,
                        "owner": "test2",
                    },
                ],
            },
            response.json(),
        )


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
        response = self.client.post("/budgets/", {"name": "test", "user": 1})
        self.assertEqual(response.status_code, 201)
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
        self.client.post("/budgets/", {"name": "test", "user": 1})
        response = self.client.post("/budgets/", {"name": "test", "user": 1})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"name": ["This field must be unique."]})

    def test_post_budget_bad_request_user_posting_on_others_user_budgets(self):
        User.objects.create_user(username="test2", password="test", email="test").save()
        self.client.login(username="test", password="test")
        response = self.client.post("/budgets/", {"name": "test", "user": 2})
        self.assertEqual(response.status_code, 400)
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
        response = self.client.get("/budgets/1/")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "Authentication credentials were not provided."},
        )

    def test_get_budget_authorized(self):
        self.client.login(username="test", password="test")
        response = self.client.get("/budgets/1/")
        self.assertEqual(response.status_code, 200)
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
        response = self.client.put("/budgets/1/", {"name": "test"})
        self.assertEqual(response.status_code, 403)
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
        self.assertEqual(response.status_code, 200)
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
        response = self.client.delete("/budgets/1/")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "Authentication credentials were not provided."},
        )

    def test_delete_budget_authorized(self):
        self.client.login(username="test", password="test")
        response = self.client.delete("/budgets/1/")
        self.assertEqual(response.status_code, 204)
