from django.db.models import TextChoices, IntegerChoices


class Breeds(TextChoices):
    CAT = 'cat'
    HEDGEHOG = 'hedgehog'


class LotStatuses(IntegerChoices):
    OPEN = 0, 'Open'
    CLOSED = 1, 'Closed'