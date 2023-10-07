from django.contrib import admin

from core.models import Budget, BudgetUser, Category, FinancialEntry

# Register your models here.

admin.site.register([Category, Budget, FinancialEntry, BudgetUser])
