from celery.utils.log import get_task_logger

from aban.celery import app, DEFAULT_QUEUE, ORDER_QUEUE, SHORT_TERMINAL_TIMEDELTA
from order.models import Currency
from order.services.order import PartialOrderServiceInterface

logger = get_task_logger(__name__)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(SHORT_TERMINAL_TIMEDELTA, task_check_partial_orders_runner.s())


@app.task(queue=DEFAULT_QUEUE)
def task_check_partial_orders_runner():
    logger.debug('Start task_check_partial_orders_runner')
    currencies = Currency.objects.active()
    for currency in currencies:
        task_check_partial_orders.delay(currency_id=currency.id)
    logger.debug('End task_check_partial_orders_runner')


@app.task(queue=ORDER_QUEUE)
def task_check_partial_orders(currency_id: int):
    logger.debug('Start task_check_partial_orders')
    currency = Currency.objects.get(id=currency_id)
    service = PartialOrderServiceInterface(currency=currency)
    service.partial_order_aggregator()
    logger.debug('End task_check_partial_orders')
