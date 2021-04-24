from django.urls import path

from api.v1.views import APIKeys
from api.v1.views import Quotes

urlpatterns = [
    path('quotes/', Quotes.as_view()),
    path('api-key/', APIKeys.as_view()),
]
