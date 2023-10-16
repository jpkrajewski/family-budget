from django.test import TestCase
from core.factories.budget_factory import BudgetFactory
from core.models import Budget


class TestBudgetFactory(TestCase):
    def setUp(self) -> None:
        for i in range(10):
            BudgetFactory()
        return super().setUp()

    def test_budget_factory(self):
        self.assertEqual(Budget.objects.count(), 10)
