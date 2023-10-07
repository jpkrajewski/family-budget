from django.contrib import admin
from core.models import Category, Budget, FinancialEntry, BudgetUser

# Register your models here.

admin.site.register([Category, Budget, FinancialEntry, BudgetUser])