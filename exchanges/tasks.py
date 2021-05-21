from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.decorators import task
from celery.utils.log import get_task_logger

from clients.alphavantage import AlphaAvantageClient
from exchanges.models import Exchanges

EXCHANGES_TO_GENERATE = (
    #('form_exchange', 'to_exchange'),
    ('USD', 'JPY')
)

logger = get_task_logger(__name__)


@task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={'max_retries': 3})
def update_exchange_data(source, destination):
    """
    Celery task to make an API call and store the exchange rate.
    If we encounter any exception we retry for 3 times with exponential backoff.
    """
    client = AlphaAvantageClient()
    try:
        exchange_rate = client.get_exchange_rate(source, destination)
    except Exception:
        logger.error(
            'Fetching exchange rate {from_exchange} - {to_exchange} failed'.format(
                from_exchange=source,
                to_exchange=destination,
            )
        )
        raise
    else:
        Exchanges.objects.create(
            from_currency=source,
            to_currency=destination,
            value=exchange_rate,
        )


@periodic_task(
    run_every=(crontab(hour='*/1')),
    name='task_fill_exchange_data',
    ignore_result=True
)
def task_fill_exchange_data():
    """
    Periodic celery task to update exchange rate
    """
    for exchange in EXCHANGES_TO_GENERATE:
        update_exchange_data.delay(exchange[0], exchange[1])
