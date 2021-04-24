from django.core.management.base import BaseCommand

from clients.alphavantage import AlphaAvantageClient
from exchanges.models import Exchanges

EXCHANGES_TO_GENERATE = (
    #('form_exchange', 'to_exchange'),
    ('USD', 'JPY')
)


class Command(BaseCommand):
    help = 'Management command to generate data for exchanges table'

    def handle(self, *args, **options):
        for exchange in EXCHANGES_TO_GENERATE:
            client = AlphaAvantageClient()
            try:
                exchange_rate = client.get_exchange_rate(exchange[0], exchange[1])
            except Exception:
                self.stdout.write(
                    self.style.ERROR(
                        'Fetching exchange rate {from_exchange} - {to_exchange} failed'.format(
                            from_exchange=exchange[0],
                            to_exchange=exchange[1],
                        )
                    )
                )
            else:
                Exchanges.objects.create(
                    from_currency=exchange[0],
                    to_currency=exchange[1],
                    value=exchange_rate,
                )
        return
