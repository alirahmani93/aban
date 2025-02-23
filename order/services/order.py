from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone
from django.utils.functional import cached_property

from order.models import Currency
from order.models.order import Order, OrderStates
from utilities.services import BaseService

from wallet.services.wallet import WalletServiceInterface, WalletReFundServiceInterface


def buy_from_exchange(value, currency):
    print(f"Buy from exchange {currency=} and {value=}")
    return True


class OrderService(BaseService):
    def __init__(self, user: User, currency: Currency, amount: Decimal, price: Decimal, ):
        super().__init__()
        self.user = user
        self.currency = currency
        self.amount = amount
        self.price = price
        self.total_price = self._get_total_price(amount=self.amount, price=self.price)
        self.irt_wallet_service = WalletServiceInterface(user=self.user, currency=self.currency.get_irt_currency())
        self.wallet_service = WalletServiceInterface(user=self.user, currency=self.currency)

    @staticmethod
    def _get_total_price(amount, price):
        return amount * price

    @cached_property
    def _check_partial(self):
        return self.total_price > settings.MIN_ORDER_VALUE

    def _get_order_state(self):
        return OrderStates.WAIT_FOR_PARTIAL if self._check_partial else OrderStates.INIT

    def _create_order(self):
        order = Order.objects.create(
            user=self.user,
            currency=self.currency,
            amount=self.amount,
            price=self.price,
            total_price=self.total_price,
            is_partial=self._check_partial,
            state=self._get_order_state(),
        )
        self.irt_wallet_service.decrease_balance(amount=self.amount)
        self.wallet_service.increase_balance(amount=self.amount)
        return order

    def _create_order_partial(self):
        self.irt_wallet_service.freezing(self.amount)
        order = Order.objects.create(
            user=self.user,
            currency=self.currency,
            amount=self.amount,
            price=self.price,
            total_price=self.total_price,
            is_partial=self._check_partial,
            state=self._get_order_state(),
            pending_at=timezone.now()
        )
        return order


class OrderServiceInterface(OrderService):
    def create_order_manager(self):
        with transaction.atomic():
            order = self._create_order_partial() if self._check_partial else self._create_order()
            self.log_debug(message=f"{self.user} create {order}")
            return order


class PartialOrderService(BaseService):
    def __init__(self, currency: Currency):
        super().__init__()
        self.currency = currency
        self.partials = Order.objects.filter_active_partials(currency=self.currency)

    def _partial_order_aggregator(self):
        self.log_info(f"start partial order calculation at {timezone.now()} for {self.currency}")
        with transaction.atomic():
            partials = self.partials.select_for_update(skip_locked=True)
            sum_partials = partials.agg_sum_active_partials()[0]["sum_partials"]
            if sum_partials < settings.MIN_ACCEPTABLE_OREDER:
                self.log_info(f"orders not enough. {sum_partials=}")
                return
            buy_from_exchange(sum_partials, self.currency)
            partials.update(state=OrderStates.SUCCEED, closed_at=timezone.now())

            wallet_refund_service = WalletReFundServiceInterface(
                user_ids=list(partials.values_list("user_id", flat=True)),
                currency=self.currency,
                partial_orders=partials
            )
            wallet_refund_service.release_funds()

            self.log_info(f"{partials.values_list('id', flat=True)} successfully closed at {timezone.now()}")


class PartialOrderServiceInterface(PartialOrderService):
    def partial_order_aggregator(self):
        self._partial_order_aggregator()
