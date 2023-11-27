from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from core.models import User, Cryptocurrency
from BuySell.models import Transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from CryptoNexa.views import update_crypto_details
from CryptoNexa.views import update_crypto_details
from core.models import Cryptocurrency, Quote

from .models import User

from collections import defaultdict


@login_required(login_url='/login/')
def portfolio(request):
    current_user = request.user
    user_id = request.user.id
    user_transactions = Transaction.objects.filter(user=current_user)
    user_object = User.objects.get(pk=user_id)

    # Crypto buy
    balance = 0

    # Crypto sold
    invested = 0

    row_amount = 0

    current_crypto_price = 'No transactions are there.'
    data = []
    for transaction in user_transactions:
        cur_data = {}
        current_crypto_price = []
        price = Cryptocurrency.objects.get(name=transaction.coin).price
        transaction_in_profit_or_loss = price - transaction.price

        row_amount = transaction.total_spent

        if transaction.type == 'buy':
            balance = balance + transaction.total_spent

        elif transaction.type == 'sell':
            invested = invested + transaction.total_spent

        cur_data['coin'] = transaction.coin
        cur_data['quantity'] = transaction.quantity
        cur_data['currency'] = transaction.currency
        cur_data['total_spent'] = row_amount
        cur_data['transaction_type'] = transaction.type
        cur_data['profit_or_loss_price'] = transaction_in_profit_or_loss
        data.append(cur_data)

    context = {
        "user_object": user_object, "data": data,
        "buy": balance,
        "sell": invested,
        "c_price": current_crypto_price,
    }

    return render(request, 'portfolio/portfolio.html', context)
