import requests
from django.http import JsonResponse
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from core.apis.coinmarketcap.dummy_data.data_usd import data_usd
from core.apis.coinmarketcap.dummy_data.data_cad import data_cad
from core.apis.coinmarketcap.dummy_data.data_jpy import data_jpy
from core.apis.coinmarketcap.dummy_data.data_inr import data_inr
from core.apis.coinmarketcap.dummy_data.data_pkr import data_pkr
from core.apis.coinmarketcap.dummy_data.data_rub import data_rub
from core.apis.coinmarketcap.dummy_data.data_kwd import data_kwd
from core.apis.coinmarketcap.dummy_data.data_eur import data_eur
from core.apis.coinmarketcap.dummy_data.data_aud import data_aud
from core.apis.coinmarketcap.dummy_data.data_nzd import data_nzd
from core.apis.coinmarketcap.dummy_data.data_aed import data_aed
from core.apis.coinmarketcap.dummy_data.data_cny import data_cny
from core.apis.coinmarketcap.dummy_data.data_v2.data_aed_2 import data_aed_2
from core.apis.coinmarketcap.dummy_data.data_v2.data_aud_2 import data_aud_2
from core.apis.coinmarketcap.dummy_data.data_v2.data_cad_2 import data_cad_2
from core.apis.coinmarketcap.dummy_data.data_v2.data_cny_2 import data_cny_2
from core.apis.coinmarketcap.dummy_data.data_v2.data_eur_2 import data_eur_2
from core.apis.coinmarketcap.dummy_data.data_v2.data_inr_2 import data_inr_2
from core.apis.coinmarketcap.dummy_data.data_v2.data_jpy_2 import data_jpy_2
from core.apis.coinmarketcap.dummy_data.data_v2.data_kwd_2 import data_kwd_2
from core.apis.coinmarketcap.dummy_data.data_v2.data_nzd_2 import data_nzd_2
from core.apis.coinmarketcap.dummy_data.data_v2.data_pkr_2 import data_pkr_2
from core.apis.coinmarketcap.dummy_data.data_v2.data_rub_2 import data_rub_2
from core.apis.coinmarketcap.dummy_data.data_v2.data_usd_2 import data_usd_2
import os

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'dd538bfb-5c46-4f03-836d-08a33c7c5e51',
}


def fetch_data(currency):
    session = Session()
    session.headers.update(headers)

    parameters = {
        'start': '1',
        'limit': '100',
        'convert': currency,
        'cryptocurrency_type': 'all',
    }

    try:
        print("Headers: ", headers)
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def convert_usd_to_cad(quote, conversion_rate=0.7324):
    cad_values = quote['USD'].copy()

    cad_values['price'] = quote['USD']['price'] * conversion_rate
    cad_values['market_cap'] = quote['USD']['market_cap'] * conversion_rate
    cad_values['fully_diluted_market_cap'] = quote['USD']['fully_diluted_market_cap'] * conversion_rate

    quote['CAD'] = cad_values

    return quote


def get_dummy_data(currency):
    if currency == "USD":
        return data_usd
    elif currency == "AUD":
        return data_aud
    elif currency == "CAD":
        return data_cad
    elif currency == "CNY":
        return data_cny
    elif currency == "EUR":
        return data_eur
    elif currency == "INR":
        return data_inr
    elif currency == "JPY":
        return data_jpy
    elif currency == "KWD":
        return data_kwd
    elif currency == "NZD":
        return data_nzd
    elif currency == "PKR":
        return data_pkr
    elif currency == "RUB":
        return data_rub
    elif currency == "AED":
        return data_aed


def get_dummy_data_2(currency):
    if currency == "USD":
        return data_usd_2
    elif currency == "AUD":
        return data_aud_2
    elif currency == "CAD":
        return data_cad_2
    elif currency == "CNY":
        return data_cny_2
    elif currency == "EUR":
        return data_eur_2
    elif currency == "INR":
        return data_inr_2
    elif currency == "JPY":
        return data_jpy_2
    elif currency == "KWD":
        return data_kwd_2
    elif currency == "NZD":
        return data_nzd_2
    elif currency == "PKR":
        return data_pkr_2
    elif currency == "RUB":
        return data_rub_2
    elif currency == "AED":
        return data_aed_2


def fetch_crypto_meta_data(symbol):
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info'

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'dd538bfb-5c46-4f03-836d-08a33c7c5e51',
    }

    session = Session()
    session.headers.update(headers)

    parameters = {
        'symbol': symbol
    }

    try:
        print("Fetching Meta Data")
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def read_currency_json():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    json_file_path = os.path.join(current_dir, 'currency_id.json')
    with open(json_file_path, 'r') as file:
        currency_data = json.load(file)
    return currency_data


def convert_prices(amount, from_id, to_id):
    price_conversion_url = 'https://pro-api.coinmarketcap.com/v2/tools/price-conversion'

    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(price_conversion_url, params={
            'amount': amount,
            'id': from_id,
            'convert_id': to_id
        })
        data = json.loads(response.text)
        # print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    return data
