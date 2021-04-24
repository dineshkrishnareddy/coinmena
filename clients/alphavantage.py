from django.conf import settings

import requests
import json
import copy
from urllib import parse


class AlphaAvantageClient:
    REQUESTS_TIMEOUT = settings.REQUESTS_TIMEOUT
    URL = 'https://www.alphavantage.co/query'
    DEFAULT_HEADERS = {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
    }

    def construct_headers(self, headers):
        _headers = copy.deepcopy(self.DEFAULT_HEADERS)
        if headers:
            _headers.update(headers)
        return _headers

    def request(self, method, headers=None, params=None, **kwargs):

        params = parse.urlencode(params)
        url = '{url}?{params}'.format(url=self.URL, params=params)
        kwargs.update({
            'url': url,
            'headers': self.construct_headers(headers),
            'timeout': self.REQUESTS_TIMEOUT,
        })
        print(url)
        import ipdb;ipdb.set_trace()
        return getattr(requests, method.lower())(**kwargs)

    def get_exchange_rate(self, from_currency='USD', to_currency='JPY'):
        response = self.request(
            method='GET',
            params={
                'function': 'CURRENCY_EXCHANGE_RATE',
                'from_currency': from_currency,
                'to_currency': to_currency,
                'apikey': settings.APIKEY,
            }
        )
        response.raise_for_status()
        content = json.loads(response.content)['Realtime Currency Exchange Rate']
        exchange_rate = 0
        for key in content.keys():
            if 'Exchange Rate' in key:
                exchange_rate = content[key]
                break
        return exchange_rate
