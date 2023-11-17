from django.shortcuts import render, redirect
from .forms import TransactionForm
from .models import Transaction
from django.contrib.auth.decorators import login_required


@login_required(login_url='/currency/')
def buysell(request, slug, name, cad_price, usd_price):
    current_currency = request.session['currency']

    initial_data = {'coin': name}
    if current_currency == 'CAD':
        initial_data['price'] = round(float(cad_price), 2)
    elif current_currency == 'USD':
        initial_data['price'] = round(float(usd_price), 2)

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

        form = TransactionForm(initial=initial_data)

    return render(request, 'BuySell/buy.html',
                  {'form': form, 'currency': current_currency, 'slug': slug, 'name': name, 'cad_price': cad_price,
                   'usd_price': usd_price})


def currency(request):
    return render(request, "BuySell/currency.html")
