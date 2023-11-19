from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from core.apis.coinmarketcap.fetch_data import fetch_data, get_dummy_data
from core.apis.helper_functions import process_crypto_data
from core.models import Cryptocurrency, Quote

from core.models import User


def index(request):
    if request.session.get('currency') is None:
        request.session['currency'] = "USD"
        session_cur = "USD"
    else:
        session_cur = request.session.get('currency')
    context = {}
    error = ''
    # fetched_data_from_api_session_cur = fetch_data(session_cur)
    fetched_data_from_api_session_cur = get_dummy_data(session_cur)
    fetched_status = fetched_data_from_api_session_cur.get('status')

    if fetched_status.get('error_code') != 0:
        error = 'An error occurred while fetching the data.'
        context['error_message'] = error
        return render(request, 'CryptoNexa/index.html', context=context)

    crypto_data = fetched_data_from_api_session_cur.get('data')
    crypto_to_send = update_crypto_details(crypto_data, session_cur)
    cryptos = process_crypto_data(crypto_to_send, session_cur, many=True)
    if request.user.id is None:
        context['cryptos'] = cryptos
    else:
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        context["user"] = user
    context['session_cur'] = session_cur
    context['cryptos'] = cryptos

    return render(request, 'CryptoNexa/index.html', context=context)


def update_crypto_details(crypto_data, session_cur):
    crypto_ids = []
    for current_crypto in crypto_data:
        quote_obj, created = Quote.objects.get_or_create(currency_slug=current_crypto.get('slug'))
        if quote_obj.data is not None and quote_obj.data.get(session_cur) is None:
            new_data = current_crypto.get('quote')
            quote_obj.data[str(session_cur)] = new_data.get(session_cur)
        else:
            quote_obj.data = current_crypto.get('quote')
        quote_obj.currency_symbol = current_crypto.get('symbol')
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

        crypto_ids.append(crypto_obj.pk)
        crypto_obj.save()

    saved_cryptos_queryset = Cryptocurrency.objects.filter(id__in=crypto_ids)
    return saved_cryptos_queryset
