from django.shortcuts import render, redirect
from .forms import TransactionForm
from .models import Transaction
from django.contrib.auth.decorators import login_required


@login_required(login_url='/currency/')
def buysell(request, name, cad_price, usd_price):

    current_currency = request.session['currency']
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.currency = request.session['currency']

            # Now, save the transaction to the database
            transaction.save()
            transaction_id = transaction.id
            # Redirect or display a success message
            return redirect('payment_checkout', transaction_id)
    else:

        initial_data = {}
        initial = initial_data
        # form.coin.initial = name
        initial_data['coin'] = name
        if (current_currency == 'CAD'):
            initial_data['price'] = float(cad_price)
        elif (current_currency == 'USD'):
            initial_data['price'] = float(usd_price)
        form = TransactionForm(initial=initial_data)


    return render(request, 'BuySell/buy.html',
                  {'form': form, 'currency': request.session['currency']})


def currency(request):
    return render(request, "BuySell/currency.html")
