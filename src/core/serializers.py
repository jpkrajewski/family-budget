from rest_framework import serializers
from core.models import Budget, Category, FinancialEntry, BudgetUser
from django.contrib.auth.models import User
from core.fields import EntriesBilanceField


class FinancialEntrySerializer(serializers.ModelSerializer):
    category = serializers.HyperlinkedRelatedField(
        queryset=Category.objects.all(),
        view_name='categories-detail'
    )
    class Meta:
        model = FinancialEntry
        fields = '__all__'

    
class FinancialEntryInCategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='financial-entries-detail')

    class Meta:
        model = FinancialEntry
        fields = ('amount', 'description', 'date', 'entry_type', 'url')

class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='categories-detail')
    bilance = EntriesBilanceField(source='financial_entries', read_only=True)
    financial_entries = FinancialEntryInCategorySerializer(
        many=True,
        read_only=True,
    )
    class Meta:
        model = Category
        fields = ('budget', 'name', 'financial_entries', 'bilance' , 'url')
        

class BudgetSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='budgets-detail')
    shared_with_users = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='users-detail'
    )
    categories = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='categories-detail'
    )
    class Meta:
        model = Budget
        fields = ('name', 'shared_with_users', 'categories', 'created_at', 'url')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
