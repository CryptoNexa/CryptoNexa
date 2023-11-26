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



def portfolio(request):

    current_user = request.user
    user_id = request.user.id
    user_transactions = Transaction.objects.filter(user=current_user)
    user_object = User.objects.get(pk=user_id)
    total = 0
    Total1 = 0
    total_sell = 0

    for transaction in user_transactions:
        if transaction.type == 'buy':

            total += transaction.quantity * transaction.price
            Total1 = total

            try:
                cryptocurrency = Cryptocurrency.objects.get(slug=transaction.coin)
                c1 = cryptocurrency.quote.data
                print(c1)
            except Cryptocurrency.DoesNotExist:
                cryptocurrency = None

            current_price = 0
            if cryptocurrency and cryptocurrency.quote:
                current_price = cryptocurrency.quote.data

            print(Total1)
        elif transaction.type == 'sell':

            total_sell += transaction.quantity * transaction.price
            total -= transaction.quantity * transaction.price
            Total2 = total
    context = {
        "user_object": user_object, "transaction_obj": user_transactions, "total": total, "buy": Total1,
        "sell": total_sell, "c_price": current_price,
    }

    return render(request, 'portfolio/portfolio.html', context)