from django.contrib.auth.forms import AuthenticationForm
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from CryptoNexa.views import update_crypto_details
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


