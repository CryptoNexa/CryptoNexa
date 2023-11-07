# Create your views here.
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from core.apis.coinmarketcap.fetch_data import fetch_data
from core.apis.coinmarketcap.test import data_usd, data_cad
from core.models import Cryptocurrency, Quote


def index(request):
    error = ''
    # fetched_data_from_api_USD = fetch_data('USD')
    fetched_data_from_api_USD = data_usd
    fetched_data_from_api_CAD = data_cad
    # fetched_data_from_api_CAD = fetch_data('CAD')
    fetched_status = fetched_data_from_api_USD.get('status')
    if fetched_status.get('error_code') != 0:
        error = 'An error occurred while fetching the data.'
        context = {
            "error_message": error
        }
        return render(request, 'crypto/crypto_list_view.html', context=context)

    crypto_data = fetched_data_from_api_USD.get('data')
    crypto_data_cad = fetched_data_from_api_CAD.get('data')
    for current_crypto in crypto_data:
        quote_obj, created = Quote.objects.get_or_create(currency_slug=current_crypto.get('slug'),

                                      currency_symbol=current_crypto.get('symbol'),
                                      data=current_crypto.get('quote'))
        quote_obj.data = current_crypto.get('quote')
        quote_obj.save()

        Cryptocurrency.objects.get_or_create(name=current_crypto.get('name'), symbol=current_crypto.get('symbol'),
                                             slug=current_crypto.get('slug'),
                                             num_market_pairs=current_crypto.get('num_market_pairs'),
                                             circulating_supply=current_crypto.get('circulating_supply'),
                                             total_supply=current_crypto.get('total_supply'),
                                             max_supply=current_crypto.get('max_supply'),
                                             infinite_supply=current_crypto.get('infinite_supply'),
                                             date_added=current_crypto.get('date_added'),
                                             last_updated=current_crypto.get('last_updated'),
                                             quote=quote_obj)

    for crypto_cad in crypto_data_cad:
        try:
            quote_obj = Quote.objects.get(currency_slug=crypto_cad.get('slug'))
            quote = quote_obj.data
            quote['CAD'] = crypto_cad.get('quote').get('CAD')
            quote_obj.save()
        except:
            pass

    cryptos = Cryptocurrency.objects.all()
    context = {
        "cryptos": cryptos
    }

    return render(request, 'CryptoNexa/index.html', context=context)
