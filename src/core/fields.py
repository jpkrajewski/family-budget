from rest_framework import serializers


class EntriesBilanceField(serializers.Field):
    def to_representation(self, value):
        bilance = 0
        for entry in value.all():
            if entry.entry_type == "Income":
                bilance += entry.amount
            else:
                bilance -= entry.amount
        return bilance
