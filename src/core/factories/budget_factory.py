from datetime import datetime

import factory

from core.factories.user_factory import UserFactory
from core.models import Budget


class BudgetFactory(factory.django.DjangoModelFactory):
    """Project model factory"""

    class Meta:
        model = Budget

    user = factory.SubFactory(UserFactory)
    name = factory.Faker("word")
    created_at = factory.Faker("date")

    # title = factory.Faker("company")
    # publisher = factory.SubFactory(UserFactory)
    # author = factory.SubFactory(UserFactory)
    # description = factory.Faker("text")
    # featured_image = ""
    # demo_link = factory.Faker("uri")
    # source_link = factory.Faker("uri")
    # created = factory.Faker("date", end_datetime=datetime.now())
    # slug = factory.Faker("slug")

    # @factory.post_generation
    # def tags(self, create, extracted, **kwargs):
    #     if not create or not extracted:
    #         return
    #     if extracted:
    #         for tag in extracted:
    #             self.tags.add(tag)
