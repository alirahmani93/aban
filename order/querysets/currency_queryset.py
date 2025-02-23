from django.db.models import Avg, Count

from utilities import BaseQuerySet, BaseManager


class CurrencyQuerySet(BaseQuerySet):

    def active(self):
        return self.filter(is_active=True)


class CurrencyManager(BaseManager):
    pass
