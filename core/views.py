from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from .apis.coinmarketcap.fetch_data import fetch_data
from .forms import CustomUserForm
from .models import Cryptocurrency, Quote


def register(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # Redirect to a success page
    else:
        form = CustomUserForm()
    return render(request, 'CryptoNexa/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')  # Redirect to a success page
    else:
        form = AuthenticationForm()
    return render(request, 'CryptoNexa/login.html', {'form': form})


def crypto_list_view(request):
    error = ''
    fetched_data_from_api = fetch_data()
    fetched_status = fetched_data_from_api.get('status')
    if fetched_status.get('error_code') != 0:
        error = 'An error occurred while fetching the data.'
        context = {
            "error_message": error
        }
        return render(request, 'crypto/crypto_list_view.html', context=context)

    crypto_data = fetched_data_from_api.get('data')

    for current_crypto in crypto_data:
        quote_obj = Quote.objects.create(currency_slug=current_crypto.get('slug'),
                                         currency_symbol=current_crypto.get('symbol'),
                                         data=current_crypto.get('quote'))

        Cryptocurrency.objects.create(name=current_crypto.get('name'), symbol=current_crypto.get('symbol'),
                                      slug=current_crypto.get('slug'), num_market_pairs=crypto_data.get('num_market_pairs'),
                                      circulating_supply=current_crypto.get('circulating_supply'), total_supply=current_crypto.get('total_supply'),
                                      max_supply=current_crypto.get('max_supply'), infinite_supply=current_crypto.get('infinite_supply'),
                                      date_added=current_crypto.get('date_added'), last_updated=current_crypto.get('last_updated'),
                                      quote=quote_obj)

    cryptos = Cryptocurrency.objects.all()
    context = {
        "cryptos": cryptos
    }
    return render(request, 'crypto/crypto_list_view.html', context=context)
