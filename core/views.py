from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render

from core.apis.coinmarketcap.fetch_data import convert_prices

# Create your views here.
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from CryptoNexa.views import update_crypto_details
from .apis.coinmarketcap.fetch_data import fetch_data
from .forms import CustomUserForm, CurrencyConverterForm
from .models import Cryptocurrency, Quote
from .forms import CustomUserForm, UserProfileForm
from .models import User
from BuySell.models import Transaction


def register(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserForm()
    return render(request, 'CryptoNexa/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'CryptoNexa/login.html', {'form': form})


def get_updated_crypto_data(request):
    updated_data = fetch_data('USD')
    update_crypto_details(updated_data)
    data = serializers.serialize("json", Cryptocurrency.objects.all())
    return JsonResponse(data)


def crypto_detail(request, slug):
    try:
        cryptocurrency = Cryptocurrency.objects.get(slug=slug)
    except Cryptocurrency.DoesNotExist:
        cryptocurrency = None

    context = {
        "cryptocurrency": cryptocurrency
    }

    return render(request, 'crypto/crypto_detail.html', context=context)


def user_logout(request):
    logout(request)
    return redirect('index')


@login_required
def user_profile(request, id):
    user = User.objects.get(id=id)
    return render(request, 'CryptoNexa/profile.html', {'user': user})


# def user_edit_profile(request, id):
#     user = User.objects.get(id=id)
#     return render(request, 'CryptoNexa/edit_profile.html', {'user': user})


@login_required
def user_edit_profile(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('core:profile', id=user.id)
    else:
        form = UserProfileForm(
            initial={'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email})

    return render(request, 'CryptoNexa/edit_profile.html', {'form': form})


def payment_history(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'CryptoNexa/payment_history.html', {
        'transactions': transactions
    })


def currency_converter(request):
    if request.method == 'POST':
        form = CurrencyConverterForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            base_currency = form.cleaned_data['base_currency']
            convert_currency = form.cleaned_data['convert_currency']

            url = "https://api.coinmarketcap.com/v2/convert"
            parameters = {
                'amount': amount,
                'symbol': base_currency,
                'convert': convert_currency,
            }

            response = requests.get(url, params=parameters)

            if response.status_code == 200:
                data = response.json()
                result = f"{amount} {base_currency} is approximately {data['data']['quotes'][convert_currency]['price']} {convert_currency}"
            else:
                result = f"Error: {response.status_code}\n{response.text}"
    else:
        form = CurrencyConverterForm()

    return render(request, "CryptoNexa/currency_converter.html", {'form': form, 'result': result})
