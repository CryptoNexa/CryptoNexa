from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


# url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
    'start': '1',
    'limit': '100',
    'convert': 'USD',
    'cryptocurrency_type': 'all',
    'tag': 'all',
    'sort': 'market_cap'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'dd538bfb-5c46-4f03-836d-08a33c7c5e51',
}


def fetch_data():
    session = Session()
    session.headers.update(headers)

    try:
        print("Headers: ", headers)
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
