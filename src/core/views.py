from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import filters
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.viewsets import ModelViewSet

from core.models import Budget, BudgetUser, Category, FinancialEntry
from core.serializers import (
    BudgetSerializer,
    BudgetUserSerializer,
    CategorySerializer,
    FinancialEntrySerializer,
    SharedBudgetSerializer,
    UserSerializer,
)


class FinancialEntryViewSet(ModelViewSet):
    queryset = FinancialEntry.objects.all()
    serializer_class = FinancialEntrySerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            filter = Q(user=user) | Q(category__budget__shared_with_users__visitor=user)
            return self.queryset.filter(filter)
        else:
            return self.queryset.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "pk"
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "name",
        "financial_entries__date",
        "financial_entries__entry_type",
        "financial_entries__amount",
    ]
    ordering_fields = ["financial_entries__date", "financial_entries__amount"]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        filter = Q(budget__user=user) | Q(budget__shared_with_users__visitor=user)
        return self.queryset.filter(filter)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class BudgetView(ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    lookup_field = "pk"
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "categories__name"]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        filter = Q(user=user) | Q(shared_with_users__visitor=user)
        return self.queryset.filter(filter)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class SharedBudgetView(ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = SharedBudgetSerializer
    lookup_field = "pk"
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "categories__name"]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(shared_with_users__visitor=user)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]


class BudgetUserViewSet(ModelViewSet):
    queryset = BudgetUser.objects.all()
    serializer_class = BudgetUserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["owner__username", "visitor__username", "budget__name"]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(owner=user)
