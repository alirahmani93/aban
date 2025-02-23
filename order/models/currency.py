from decimal import Decimal

from django.db import models

from order.choices import CurrencyCodes
from order.querysets.currency_queryset import CurrencyQuerySet, CurrencyManager
from utilities import BaseModel
from utilities.fields.decimal import CurrencyDecimalField



class Currency(BaseModel):
    name = models.CharField(max_length=32)
    code = models.CharField(max_length=10, choices=CurrencyCodes.choices, unique=True)
    price = CurrencyDecimalField(default=Decimal(4))

    objects = CurrencyManager.from_queryset(CurrencyQuerySet)()

    def __str__(self):
        return f"{self.name} {self.price}"

    @classmethod
    def get_irt_currency(self):
        return Currency.objects.get(code=CurrencyCodes.IRT)