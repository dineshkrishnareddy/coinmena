from django.urls import path

from api.v1.views import Quotes

urlpatterns = [
    path('quotes/', Quotes.as_view()),
]
