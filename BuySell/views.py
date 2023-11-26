from django.shortcuts import render, redirect
from .forms import TransactionForm
from .models import Transaction
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def buysell(request, slug, name, price):
    current_currency = request.session['currency']

    initial_data = {'coin': name}
    initial_data['price'] = round(float(price), 4)
    # Adding 3% Transaction Fee
    initial_data['transaction_fee'] = round(float(initial_data['price']) * 0.03, 4)

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
                  {'form': form, 'currency': current_currency, 'slug': slug, 'name': name, 'price': price})


def currency(request):
    return render(request, "BuySell/currency.html")
