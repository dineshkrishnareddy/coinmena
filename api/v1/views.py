from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_api_key.models import APIKey
from rest_framework_api_key.permissions import HasAPIKey

from exchanges.models import Exchanges
from clients.alphavantage import AlphaAvantageClient


class Quotes(APIView):
    permission_classes = [HasAPIKey]

    def get(self, request):
        from_currency = request.GET.get('from_currency', 'USD')
        to_currency = request.GET.get('to_currency', 'JPY')
        data = Exchanges.objects.filter(
            from_currency=from_currency,
            to_currency=to_currency,
        ).last()
        return Response(
            data=data,
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        from_currency = request.POST.get('from_currency', 'USD')
        to_currency = request.POST.get('to_currency', 'JPY')
        client = AlphaAvantageClient()
        try:
            exchange_rate = client.get_exchange_rate(
                from_currency=from_currency,
                to_currency=to_currency,
            )
        except:
            return Response(
                data={'detail': 'Category is not Used Cars'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            data={
                from_currency: from_currency,
                to_currency: to_currency,
                exchange_rate: exchange_rate,
            },
            status=status.HTTP_201_CREATED,
        )


class APIKeys(APIView):

    def get(self, request):
        key_name = request.GET.get('key_name', 'default')
        key = APIKey.objects.get(name=key_name)
        return Response(
            data=key,
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        key_name = request.POST.get('key_name', 'default')
        _, key = APIKey.objects.create_key(name=key_name)
        return Response(
            data=key,
            status=status.HTTP_201_CREATED,
        )
