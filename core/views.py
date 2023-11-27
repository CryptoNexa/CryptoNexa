from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from CryptoNexa.views import update_crypto_details
from .apis.coinmarketcap.fetch_data import fetch_data, get_dummy_data, get_dummy_data_2
from .apis.helper_functions import process_crypto_data
from .models import Cryptocurrency, Watchlist
from .forms import CustomUserForm, UserProfileForm, WatchlistForm
from .models import User
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


def get_updated_crypto_data(request, fetch_live_data):
    switch = request.session.get('switch')
    if switch is None:
        request.session['switch'] = 0
        switch = 0

    if request.session.get('currency') is None:
        request.session['currency'] = "USD"
        session_cur = "USD"
    else:
        session_cur = request.session.get('currency')

    if fetch_live_data:
        fetched_data_from_api_session_cur = fetch_data(session_cur)
    else:
        if int(switch) == 0:
            request.session['switch'] = 1

            fetched_data_from_api_session_cur = get_dummy_data_2(session_cur)
        else:
            request.session['switch'] = 0
            fetched_data_from_api_session_cur = get_dummy_data(session_cur)

    crypto_data = fetched_data_from_api_session_cur.get('data')
    crypto_to_send = update_crypto_details(crypto_data, session_cur)
    crypto_data = process_crypto_data(crypto_to_send, session_cur, many=True)
    print("Updated price returned")
    return JsonResponse(crypto_data, safe=False)


def crypto_detail(request, slug):
    try:
        cryptocurrency = Cryptocurrency.objects.get(slug=slug)
    except Cryptocurrency.DoesNotExist:
        cryptocurrency = None

    if request.session.get('currency') is None:
        request.session['currency'] = "USD"
        session_cur = "USD"
    else:
        session_cur = request.session.get('currency')

    data = process_crypto_data(cryptocurrency, session_cur, many=False)

    context = {
        "cryptocurrency": data,
        "session_cur": session_cur
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
    user = get_object_or_404(User, id=id)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            # Save the form data
            form.save()

            return redirect('index')
        else:
            return HttpResponseBadRequest("Invalid form submission. Please check the form data.")
    else:
        form = UserProfileForm(
            initial={'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email,
                     'photo_id': user.photo_id})

    return render(request, 'CryptoNexa/edit_profile.html', {'form': form})


@login_required
def watchlist(request, watchlist_id=None):
    session_currency = request.session.get('currency')
    user_watchlists = Watchlist.objects.filter(user=request.user)
    if request.method == 'POST':
        form = WatchlistForm(request.POST)
        if form.is_valid():
            watchlist = get_object_or_404(Watchlist, id=watchlist_id, user=request.user)
            watchlist.cryptocurrencies.set(form.cleaned_data['cryptocurrencies'])
            watchlist.save()
            return redirect('core:watchlist', watchlist_id=watchlist.id)
        else:
            print("Form errors:", form.errors)
    else:
        form = WatchlistForm()
        if watchlist_id:
            selected_watchlist = get_object_or_404(Watchlist, id=watchlist_id)
            cryptocurrencies = selected_watchlist.cryptocurrencies.all()

            form.fields['cryptocurrencies'].initial = cryptocurrencies

    if not user_watchlists.exists():
        default_watchlist = Watchlist.objects.create(user=request.user, name='My Watchlist')
        form = WatchlistForm(instance=default_watchlist)
        user_watchlists = Watchlist.objects.filter(user=request.user)

    if watchlist_id:
        selected_watchlist = get_object_or_404(Watchlist, id=watchlist_id)
        cryptocurrencies = selected_watchlist.cryptocurrencies.all()
    else:
        selected_watchlist = user_watchlists.first()
        cryptocurrencies = selected_watchlist.cryptocurrencies.all()

    data = process_crypto_data(cryptocurrencies, session_currency, many=True)
    print(data)
    return render(request, 'CryptoNexa/watchlist.html',
                  {'form': form, 'user_watchlists': user_watchlists, 'selected_watchlist': selected_watchlist,
                   'cryptocurrencies': data, 'session_cur': session_currency})


@login_required
def create_watchlist(request):
    watchlist = Watchlist.objects.create(user=request.user, name='My New Watchlist')

    return redirect('core:watchlist', watchlist_id=watchlist.id)


@login_required
def edit_watchlist_name(request, watchlist_id):
    if request.method == 'POST':
        form = WatchlistForm(request.POST)
        if form.is_valid():
            watchlist = get_object_or_404(Watchlist, id=watchlist_id, user=request.user)
            watchlist.name = form.cleaned_data['name']
            watchlist.save()
            return redirect('core:watchlist', watchlist_id=watchlist_id)
        else:
            print(form.errors)

    return redirect('core:watchlist', watchlist_id=watchlist_id)


def payment_history(request):
    transactions = Transaction.objects.filter(user=request.user)

    # Handle search
    search_query = request.GET.get('search')
    if search_query:
        transactions = transactions.filter(
            Q(type__icontains=search_query) |
            Q(coin__icontains=search_query) |
            Q(currency__icontains=search_query) |
            Q(quantity__icontains=search_query) |
            Q(price__icontains=search_query) |
            Q(total_spent__icontains=search_query) |
            Q(datetime__icontains=search_query) |
            Q(transaction_fee__icontains=search_query) |
            Q(notes__icontains=search_query) |
            Q(status__icontains=search_query)
        )
    # Handle status filter
    status_filter = request.GET.get('status')
    if status_filter:
        transactions = transactions.filter(status=status_filter)

    print("transactions = ", transactions)

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
            has_error = True
            error_msg = "Value should be greater than or equal to 1"
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
