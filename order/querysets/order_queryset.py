from django.db.models import Avg, Count, Sum

from order.models import Currency
from order.models.order import OrderStates
from utilities import BaseQuerySet, BaseManager


class OrderQuerySet(BaseQuerySet):

    def active(self):
        return self.filter(is_active=True)

    def partials(self, currency: "Currency"):
        return self.filter(is_partial=True, state=OrderStates.WAIT_FOR_PARTIAL, currency=currency)


class OrderManager(BaseManager):
    def filter_active_partials(self, currency: "Currency"):
        return self.active().partials(currency=currency)

    def agg_sum_active_partials(self):
        return self.values("total_price").aggregate(sum_partials=Sum("total_price"))
