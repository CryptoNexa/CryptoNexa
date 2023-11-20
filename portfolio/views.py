from django.shortcuts import render
from core.models import User, Cryptocurrency
from BuySell.models import Transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404

def portfolio(request):

    current_user = request.user
    user_id = request.user.id
    user_transactions = Transaction.objects.filter(user=current_user)
    user_object = User.objects.get(pk=user_id)

    total = sum(transaction.quantity * transaction.price for transaction in user_transactions)
    context = {
        "user_object": user_object, "transaction_obj": user_transactions, "total": total
    }
    return render(request, 'portfolio/portfolio.html', context)
