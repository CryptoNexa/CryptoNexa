from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from core.apis.coinmarketcap.fetch_data import fetch_data, convert_usd_to_cad
from core.models import Cryptocurrency, Quote


def index(request):
    error = ''
    fetched_data_from_api_USD = fetch_data('USD')
    # fetched_data_from_api_USD = data_usd
    fetched_status = fetched_data_from_api_USD.get('status')
    if fetched_status.get('error_code') != 0:
        error = 'An error occurred while fetching the data.'
        context = {
            "error_message": error
        }
        return render(request, 'crypto/crypto_list_view.html', context=context)

    crypto_data = fetched_data_from_api_USD.get('data')
    update_crypto_details(crypto_data)
    cryptos = Cryptocurrency.objects.all()
    context = {
        "cryptos": cryptos
    }

    return render(request, 'CryptoNexa/index.html', context=context)


def update_crypto_details(crypto_data):
    for current_crypto in crypto_data:
        quote_obj, created = Quote.objects.get_or_create(currency_slug=current_crypto.get('slug'))
        quote_obj.currency_symbol = current_crypto.get('symbol')
        quote_obj.data = convert_usd_to_cad(current_crypto.get('quote'))
        quote_obj.save()

        try:
            crypto_obj = Cryptocurrency.objects.get(slug=current_crypto.get('slug'))
            crypto_obj.quote = quote_obj
        except ObjectDoesNotExist as e:
            crypto_obj = Cryptocurrency.objects.create(slug=current_crypto.get('slug'), quote=quote_obj)
        crypto_obj.name = current_crypto.get('name')
        crypto_obj.symbol = current_crypto.get('symbol')
        crypto_obj.num_market_pairs = current_crypto.get('num_market_pairs')
        crypto_obj.circulating_supply = current_crypto.get('circulating_supply')
        crypto_obj.total_supply = current_crypto.get('total_supply')
        crypto_obj.max_supply = current_crypto.get('max_supply')
        crypto_obj.infinite_supply = current_crypto.get('infinite_supply')
        crypto_obj.date_added = current_crypto.get('date_added')
        crypto_obj.last_updated = current_crypto.get('last_updated')
        crypto_obj.save()

