from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f"Budget: {self.name} ({self.user.username})"


class Category(models.Model):
    name = models.CharField(max_length=100)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return f"Category: {self.name}"


class FinancialEntry(models.Model):
    ENTRY_TYPES = (
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='financial_entries')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateField()
    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPES)

    def __str__(self):
        return f"{self.entry_type}: {self.amount} ({self.date})"
    

class BudgetUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='shared_with_users')

    class Meta:
        unique_together = ('user', 'budget')

    def __str__(self):
        return f"{self.user.username} in {self.budget.name}"
    
    def save(self, *args, **kwargs):
        # Check if a budget with the primary user already exists
        existing_budget = Budget.objects.filter(user=self.user).first()
        if existing_budget:
            raise Exception(f"A budget with the primary user already exists ({self.user.username}).")
        super().save(*args, **kwargs)
