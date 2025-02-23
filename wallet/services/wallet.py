from decimal import Decimal
from typing import List

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F

from order.models import Currency
from order.models.currency import CurrencyCodes
from order.models.order import Order
from utilities.services import BaseService
from wallet.models.wallet import Wallet


class WalletService(BaseService):
    def __init__(self, user, currency, ):
        super().__init__()
        self.user = user
        self.currency = currency
        self.wallet = self._find_wallet()

    def _find_wallet(self):
        with transaction.atomic:
            wallet = Wallet.objects.filter(user=self.user, currency=self.currency)
            if wallet.exists():
                wallet = wallet.select_for_update(skip_locked=True).first()
            wallet.create(user=self.user, currency=self.currency)

    def _increase_balance(self, amount: Decimal):
        self.wallet.balance += amount
        return self.wallet

    def _decrease_balance(self, amount: Decimal):
        self.wallet.balance -= amount
        return self.wallet

    def _freezing(self, amount: Decimal):
        if self.wallet.balance < amount and self.wallet.balance - amount < 0:
            raise ValidationError("Not enough balance.")
        self.wallet.balance -= amount
        self.wallet.freeze += amount


class WalletServiceInterface(WalletService):
    def increase_balance(self, amount: Decimal):
        self._increase_balance(amount)
        self.wallet.save()
        self.log_debug(message=f"{self.user} increase {amount} from {self.wallet} ")

    def decrease_balance(self, amount: Decimal):
        self._decrease_balance(amount)
        self.wallet.save()
        self.log_debug(message=f"{self.user} decrease {amount} from {self.wallet} ")

    def freezing(self, amount: Decimal):
        self._freezing(amount)
        self.wallet.save()
        self.log_debug(message=f"{self.user} freeze {amount} from {self.wallet} ")


from decimal import Decimal


class WalletReFundService(BaseService):
    def __init__(self, user_ids: list, currency: Currency, partial_orders: Order):
        super().__init__()
        self.currency = currency
        self.partial_orders = partial_orders

        self.wallets = Wallet.objects.select_for_update().filter(
            user_id__in=user_ids,
            currency=currency
        ).select_related('user')

        self.irt_wallets = Wallet.objects.select_for_update().filter(
            user_id__in=user_ids,
            currency__code=CurrencyCodes.IRT # should be impl in WalletQueryset for irt currency
        ).select_related('user')

    def _validate_state(self):
        """Validate initial state before processing."""
        if not self.wallets.exists():
            raise ValidationError("No wallets found for the given criteria")
        if not self.irt_wallets.exists():
            raise ValidationError("No IRT wallets found")

    def _calculate_total_amount(self):
        """Calculate total amount to process from partial orders."""
        return sum(order.amount for order in self.partial_orders)

    def _un_freeze_irt_wallet(self):
        """Unfreeze IRT wallet balances."""
        total_amount = self._calculate_total_amount()
        self.irt_wallets.update(frozen_balance=F('frozen_balance') - total_amount)

    def _increase_currency_wallet_balance(self):
        """Increase balance for target currency wallets."""
        total_amount = self._calculate_total_amount()
        self.wallets.update(balance=F('balance') + total_amount)

class WalletReFundServiceInterface(WalletReFundService):

    def release_funds(self):
        """Main method to process fund releases."""
        try:
            self._validate_state()

            with transaction.atomic():
                self._un_freeze_irt_wallet()
                self._increase_currency_wallet_balance()

                self.log_debug(
                    message=f"Funds released successfully. "
                            f"Impacted wallet IDs: {list(self.wallets.values_list('id', flat=True))}. "
                            f"IRT wallet IDs: {list(self.irt_wallets.values_list('id', flat=True))}"
                )

        except ValidationError as e:
            self.log_error(f"Validation error: {str(e)}")
            raise e
        except Exception as e:
            self.log_error(f"Unexpected error during fund release: {str(e)}")
            raise e
