from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from core.views import BudgetView, CategoryViewSet, FinancialEntryViewSet, UserViewSet


router = DefaultRouter()
router.register('financial-entries', FinancialEntryViewSet, basename='financial-entries')
router.register('categories', CategoryViewSet, basename='categories')
router.register('budgets', BudgetView, basename='budgets')
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]