import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from auction.core import constants


class UserFactory(DjangoModelFactory):
    username = factory.Faker('user_name')

    class Meta:
        model = 'auth.User'
        django_get_or_create = ('username',)

    @factory.post_generation
    def password(obj, create, extracted, **kwargs):
        if not create:
            return
        obj.set_password(extracted or 'password')
        obj.save()


class UserAccountFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    balance = factory.Faker('pydecimal', left_digits=8, right_digits=2, positive=True,)

    class Meta:
        model = 'core.UserAccount'


class PetFactory(DjangoModelFactory):
    name = factory.Faker('name')
    breed = FuzzyChoice(constants.Breeds.choices, getter=lambda c: c[0])
    owner = factory.SubFactory(UserAccountFactory)

    class Meta:
        model = 'core.Pet'


class LotFactory(DjangoModelFactory):
    pet = factory.SubFactory(PetFactory)
    author = factory.SubFactory(UserAccountFactory)
    price = factory.Faker('pydecimal', left_digits=8, right_digits=2, positive=True,)
    status = FuzzyChoice(constants.LotStatuses.choices, getter=lambda c: c[0])

    class Meta:
        model = 'core.Lot'


class BidFactory(DjangoModelFactory):
    lot = factory.SubFactory(LotFactory)
    author = factory.SubFactory(UserAccountFactory)
    price = factory.Faker('pydecimal', left_digits=8, right_digits=2, positive=True,)

    class Meta:
        model = 'core.Bid'