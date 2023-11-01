# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render


def index(request):
    cryptos = [
        {
            "name": "Bitcoin",
            "Price": 34500,
            "oneHour": "0.27%",
            "oneHourFlag": -1,
            "TwentyFourHour": "0.67",
            "TwentyFourHourFlag": -1,
            "MarketCap": "673,506,667,886",
            "Volume": "17,354,758,340"
        },
        {
            "name": "Ethereum",
            "Price": 2600,
            "oneHour": "0.42%",
            "oneHourFlag": 1,
            "TwentyFourHour": "1.25%",
            "TwentyFourHourFlag": 1,
            "MarketCap": "300,456,789,123",
            "Volume": "10,456,123,789"
        },
        {
            "name": "Ripple",
            "Price": 1.23,
            "oneHour": "0.11%",
            "oneHourFlag": -1,
            "TwentyFourHour": "0.75%",
            "TwentyFourHourFlag": -1,
            "MarketCap": "56,789,123,456",
            "Volume": "2,345,678,901"
        },
        {
            "name": "Litecoin",
            "Price": 155,
            "oneHour": "0.33%",
            "oneHourFlag": 1,
            "TwentyFourHour": "0.85%",
            "TwentyFourHourFlag": 1,
            "MarketCap": "12,345,678,901",
            "Volume": "567,890,123"
        },
        {
            "name": "Cardano",
            "Price": 2.45,
            "oneHour": "0.28%",
            "oneHourFlag": 1,
            "TwentyFourHour": "0.92%",
            "TwentyFourHourFlag": 1,
            "MarketCap": "7,890,123,456",
            "Volume": "345,678,901"
        }
    ]

    context = {
        "cryptos": cryptos
    }
    return render(request, 'CryptoNexa/index.html', context=context)

