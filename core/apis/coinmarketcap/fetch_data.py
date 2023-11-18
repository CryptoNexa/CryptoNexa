from django.http import JsonResponse
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


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
