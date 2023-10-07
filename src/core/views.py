from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response 
from core.models import Budget, Category, FinancialEntry
from django.contrib.auth.models import User
from rest_framework import filters
from core.serializers import BudgetSerializer, CategorySerializer, FinancialEntrySerializer, UserSerializer

class FinancialEntryViewSet(ModelViewSet):
    queryset = FinancialEntry.objects.all()
    serializer_class = FinancialEntrySerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'financial_entries__date', 'financial_entries__entry_type', 'financial_entries__amount']
    ordering_fields = ['financial_entries__date', 'financial_entries__amount']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Get budgets associated with the authenticated user
            user_budgets = user.budgets.all()
            # Filter categories where the budget is in the user's budgets
            return self.queryset.filter(budget__in=user_budgets)
        else:
            return self.queryset.none()

class BudgetView(ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    lookup_field = 'pk'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'categories__name']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return self.queryset.filter(user=user)
        else:
            return self.queryset.none()
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, serializer):
        serializer.delete(user=self.request.user)


        



class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    


