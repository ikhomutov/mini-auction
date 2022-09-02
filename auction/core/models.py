from decimal import Decimal

from django.db import models
from django.db.models.functions import Coalesce

from .constants import Breeds, LotStatuses


class UserAccount(models.Model):
    """
    Represents data related to a specific user.
    This way we can keep default User model and add extra logic
    """
    user = models.OneToOneField(
        to='auth.User', on_delete=models.PROTECT
    )
    balance = models.DecimalField(
        max_digits=10, decimal_places=2
    )

    def __str__(self):
        return self.user.username

    @property
    def available_balance(self):
        open_bids_sum = self.bids.filter(
            lot__status=LotStatuses.OPEN
        ).aggregate(
            price_sum=Coalesce(models.Sum('price'), Decimal('0.00'))
        )['price_sum']
        return self.balance - open_bids_sum

    def increase_balance(self, amount):
        self.balance += amount
        self.save()

    def decrease_balance(self, amount):
        self.balance -= amount
        self.save()


class Pet(models.Model):
    breed = models.CharField(
        max_length=50, choices=Breeds.choices
    )
    owner = models.ForeignKey(
        to=UserAccount, on_delete=models.CASCADE, related_name='pets'
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def set_owner(self, new_owner):
        self.owner = new_owner
        self.save()


class Lot(models.Model):
    pet = models.ForeignKey(
        to=Pet, on_delete=models.PROTECT
    )
    author = models.ForeignKey(
        to=UserAccount, on_delete=models.PROTECT, related_name='lots'
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2
    )
    status = models.PositiveSmallIntegerField(
        choices=LotStatuses.choices
    )
    created_at = models.DateTimeField(auto_now=True)

    @property
    def is_closed(self):
        return self.status == LotStatuses.CLOSED

    def close(self):
        self.status = LotStatuses.CLOSED
        self.save()


class Bid(models.Model):
    author = models.ForeignKey(
        to=UserAccount, on_delete=models.PROTECT, related_name='bids'
    )
    lot = models.ForeignKey(
        to=Lot, on_delete=models.PROTECT, related_name='bids'
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2
    )
    created_at = models.DateTimeField(auto_now=True)
