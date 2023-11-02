from django.shortcuts import render
from .models import Currency


# Create your views here.
def currency_exchange(request):
    currencies = Currency.objects.all()
    context = {
        "currencies": currencies
    }

    return render(request, 'currencyExchange/currency_exchange_view.html', context)
