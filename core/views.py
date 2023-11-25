from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core import serializers
from django.http import JsonResponse
from core.apis.coinmarketcap.fetch_data import convert_prices, read_currency_json

from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from CryptoNexa.views import update_crypto_details
from .apis.coinmarketcap.fetch_data import fetch_data
from .forms import CurrencyConverterForm, CustomUserForm, UserProfileForm
from .models import Cryptocurrency, User
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
    resulted_price = 0
    has_error = False
    error_msg = ""
    currency_data = read_currency_json()

    if request.method == 'POST':
        form = CurrencyConverterForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            base_currency = form.cleaned_data['base_currency']
            convert_currency = form.cleaned_data['convert_currency']
            from_id = currency_data.get(base_currency, {}).get('ConvertID')
            to_id = currency_data.get(convert_currency, {}).get('ConvertID')
            if from_id and to_id:
                result = convert_prices(amount, from_id, to_id)
                if result["data"]:
                    resulted_price = result["data"]["quote"][str(to_id)]["price"]
                else:
                    has_error = True
                    error_msg = result["status"]["error_message"]
    else:
        form = CurrencyConverterForm()

    form_data = {
        'amount': request.POST.get('amount', form['amount'].value() or 1),
        'base_currency': request.POST.get('base_currency', form['base_currency'].value()),
        'convert_currency': request.POST.get('convert_currency', form['convert_currency'].value())
    }

    return render(request, "CryptoNexa/currency_converter.html",
                  {'form': form, 'resulted_price': resulted_price, 'currency_data': currency_data,
                   'form_data': form_data, 'error_msg': error_msg, 'hasError': has_error})
