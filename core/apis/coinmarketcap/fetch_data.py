import requests
from django.http import JsonResponse
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
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
