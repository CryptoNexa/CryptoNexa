from django.shortcuts import render, redirect
from .forms import TransactionForm
from .models import Transaction
from django.contrib.auth.decorators import login_required


@login_required(login_url='/currency/')
def buysell(request):
    COIN_TYPES = [
        ('bitcoin', "Bitcoin BTC"),
        ('ethereum', "Ethereum ETH"),
    ]
    request.session['currency'] = "CAD"
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.currency = request.session['currency']

            # Now, save the transaction to the database
            transaction.save()
            # Redirect or display a success message
            return redirect('currency')
    else:
        form = TransactionForm()
    return render(request, 'BuySell/buy.html', {'form': form, 'currency': request.session['currency'], 'COIN_TYPES': COIN_TYPES}, )

def currency(request):
    return render(request, "BuySell/currency.html")
