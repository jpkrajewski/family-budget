from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from core.fields import EntriesBilanceField
from core.models import Budget, BudgetUser, Category, FinancialEntry


class FinancialEntrySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="financial-entries-detail")
    category = serializers.HyperlinkedRelatedField(
        queryset=Category.objects.all(), view_name="categories-detail"
    )

    class Meta:
        model = FinancialEntry
        fields = "__all__"

    def validate(self, attrs):
        if attrs["category"].budget.user != self.context["request"].user:
            raise ValidationError("This budget doesn't belong to you.")
        return attrs


class FinancialEntryInCategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="financial-entries-detail")

    class Meta:
        model = FinancialEntry
        fields = ("amount", "description", "date", "entry_type", "url")


class CategorySerializer(serializers.ModelSerializer):
    budget = serializers.HyperlinkedRelatedField(
        queryset=Budget.objects.all(), view_name="budgets-detail"
    )
    url = serializers.HyperlinkedIdentityField(view_name="categories-detail")
    bilance = EntriesBilanceField(source="financial_entries", read_only=True)
    financial_entries = FinancialEntryInCategorySerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Category
        fields = ("budget", "name", "financial_entries", "bilance", "url")

    def validate(self, attrs):
        if attrs["budget"].user != self.context["request"].user:
            raise ValidationError("This budget doesn't belong to you.")
        return attrs


class BudgetUsersInBudgetSerializer(serializers.ModelSerializer):
    visitor = serializers.HyperlinkedRelatedField(
        view_name="users-detail", read_only=True
    )

    class Meta:
        model = BudgetUser
        fields = ("visitor",)


class BudgetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="user.username")
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=Budget.objects.all())]
    )
    url = serializers.HyperlinkedIdentityField(view_name="budgets-detail")
    shared_with_users = BudgetUsersInBudgetSerializer(many=True, read_only=True)
    categories = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="categories-detail"
    )

    class Meta:
        model = Budget
        fields = (
            "owner",
            "user",
            "name",
            "shared_with_users",
            "categories",
            "created_at",
            "url",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data["user"] != self.context["request"].user:
            raise serializers.ValidationError("You cannot change the user.")
        return super().update(instance, validated_data)

    def validate(self, attrs):
        if attrs["user"] != self.context["request"].user:
            raise ValidationError("This budget doesn't belong to you.")
        return super().validate(attrs)


class SharedBudgetSerializer(BudgetSerializer):
    name = serializers.ReadOnlyField()

    def validate(self, attrs):
        raise serializers.ValidationError("You cannot create shared budget this way.")


class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ["id", "username"]


class BudgetUserSerializer(serializers.ModelSerializer):
    validators = [
        UniqueTogetherValidator(
            queryset=BudgetUser.objects.all(), fields=["owner", "visitor", "budget"]
        )
    ]
    owner_name = serializers.ReadOnlyField(source="owner.username")
    visitor_name = serializers.ReadOnlyField(source="visitor.username")
    visitor = serializers.HyperlinkedRelatedField(
        view_name="users-detail", queryset=User.objects.all()
    )
    budget_name = serializers.ReadOnlyField(source="budget.name")

    class Meta:
        model = BudgetUser
        fields = "__all__"

    def validate(self, attrs):
        request = self.context.get("request")
        attrs["owner"] = request.users
        if attrs["owner"] == attrs["visitor"]:
            raise ValidationError("You can't share budget with yourself.")
        if attrs["budget"].user != attrs["owner"]:
            raise ValidationError("This budget doesn't belong to you.")
        return super().validate(attrs)

    # 5?NUFZ^3#6fNw2+
