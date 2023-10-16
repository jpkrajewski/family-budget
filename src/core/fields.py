from rest_framework import serializers
from core.models import FinancialEntry


class EntriesBilanceField(serializers.Field):
    def to_representation(self, value):
        bilance = 0
        for entry in value.all():
            if FinancialEntry.INCOME == entry.entry_type:
                bilance += entry.amount
            if FinancialEntry.EXPENSE == entry.entry_type:
                bilance -= entry.amount
        return bilance
