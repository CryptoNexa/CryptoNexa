import decimal

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from CryptoNexa.forms import CryptoFilterForm
from core.apis.helper_functions import process_crypto_data, keep_two_chars_after_dot
from core.apis.coinmarketcap.fetch_data import fetch_data, get_dummy_data
from core.models import Cryptocurrency, Quote
from django.shortcuts import render
from core.apis.coinmarketcap.fetch_data import fetch_data, convert_usd_to_cad
from core.models import Cryptocurrency, Quote, FooterList

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
    context['update_values'] = True
    context['filters_provided'] = False
    footer_items = FooterList.objects.all()
    context['footer_items'] = footer_items

    return render(request, 'CryptoNexa/index.html', context=context)


def update_crypto_details(crypto_data, session_cur, filters=None):
    if filters:
        filtered_crypto = Cryptocurrency.objects.all()

        if filters.get('name') is not None and filters.get('name') != "":
            filtered_crypto = filtered_crypto.filter(slug__contains=filters.get('name').lower())

        if filters.get('num_market_pairs') is not None:
            filtered_crypto = filtered_crypto.filter(slug=filters.get('num_market_pairs'))

        if filters.get('circulating_supply') is not None:
            filtered_crypto = filtered_crypto.filter(circulating_supply=filters.get('circulating_supply'))

        if filters.get('total_supply') is not None:
            filtered_crypto = filtered_crypto.filter(total_supply=filters.get('total_supply'))

        if filters.get('max_supply') is not None:
            filtered_crypto = filtered_crypto.filter(max_supply=filters.get('max_supply'))

        if filters.get('price_min') is not None:
            filtered_crypto = filtered_crypto.filter(price__gt=filters.get('price_min'))

        if filters.get('price_max') is not None:
            filtered_crypto = filtered_crypto.filter(price__lt=filters.get('price_max'))


        if filters.get('infinite_supply') == "True":
            filtered_crypto = filtered_crypto.filter(infinite_supply=True)
        elif filters.get('infinite_supply') == "False":
            filtered_crypto = filtered_crypto.filter(infinite_supply=False)


        return filtered_crypto

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
        price = float(current_crypto.get('quote').get(session_cur).get('price'))
        price = "{:.2f}".format(price)
        crypto_obj.price = price
        crypto_ids.append(crypto_obj.pk)
        crypto_obj.save()

    saved_cryptos_queryset = Cryptocurrency.objects.filter(id__in=crypto_ids)
    return saved_cryptos_queryset


def filter_crypto_data(request):
    if request.session.get('currency') is None:
        request.session['currency'] = "USD"
        session_cur = "USD"
    else:
        session_cur = request.session.get('currency')
    context = {}
    if request.method == "POST":
        submitted_form = CryptoFilterForm(request.POST)
        if not submitted_form.is_valid():
            return render(request, 'crypto/crypto_list_filter_modal.html', {"form": submitted_form})

        fetched_data_from_api_session_cur = get_dummy_data(session_cur)
        fetched_status = fetched_data_from_api_session_cur.get('status')

        if fetched_status.get('error_code') != 0:
            error = 'An error occurred while fetching the data.'
            context['error_message'] = error
            return render(request, 'CryptoNexa/index.html', context=context)

        crypto_data = fetched_data_from_api_session_cur.get('data')
        crypto_to_send = update_crypto_details(crypto_data, session_cur, filters=submitted_form.cleaned_data)
        cryptos = process_crypto_data(crypto_to_send, session_cur, many=True)
        context['update_values'] = False
        context['cryptos'] = cryptos
        context['filters_provided'] = True
        context['session_cur'] = session_cur
        context['crypto_count'] = len(cryptos)
        return render(request, 'CryptoNexa/index.html', context=context)

    else:
        form = CryptoFilterForm()

    context['form'] = form
    return render(request, 'crypto/crypto_list_filter_modal.html', context)
