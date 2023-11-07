from django.urls import path
from .views import CurrencyList, CurrencyDetail

urlpatterns = [
    path("currencies/", CurrencyList.as_view(), name="currencies"),
    path("currency/<int:id>/", CurrencyDetail.as_view(), name="currency_detail"),
]
