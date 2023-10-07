from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.views import (
    BudgetUserViewSet,
    BudgetView,
    CategoryViewSet,
    FinancialEntryViewSet,
    SharedBudgetView,
    UserViewSet,
)

router = DefaultRouter()
router.register(
    "financial-entries", FinancialEntryViewSet, basename="financial-entries"
)
router.register("categories", CategoryViewSet, basename="categories")
router.register("budgets", BudgetView, basename="budgets")
router.register("shared-budgets", SharedBudgetView, basename="shared-budgets")
router.register("users", UserViewSet, basename="users")
router.register("budget-users", BudgetUserViewSet, basename="budget-users")


urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
