from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budgets")
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Budget: {self.name} ({self.user.username})"


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=100)
    budget = models.ForeignKey(
        Budget, on_delete=models.CASCADE, related_name="categories"
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"Category: {self.name}"


class FinancialEntry(models.Model):
    ENTRY_TYPES = (
        ("Income", "Income"),
        ("Expense", "Expense"),
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="financial_entries"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="financial_entries"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateField()
    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPES)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.entry_type}: {self.amount} ({self.date})"


class BudgetUser(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="owners")
    visitor = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="visitors"
    )
    budget = models.ForeignKey(
        Budget, on_delete=models.DO_NOTHING, related_name="shared_with_users"
    )

    class Meta:
        unique_together = ("owner", "visitor")
        ordering = ["owner", "visitor"]

    def __str__(self):
        return f"{self.owner.username} shared {self.budget.name} to {self.visitor.username}"
