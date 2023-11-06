import json
import time

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import UserPayment
from django.views import View
from BuySell.models import Transaction
from django.shortcuts import get_object_or_404
from core.models import User
import stripe

# Create your views here.
stripe.api_key = settings.STRIPE_PRIVATE_KEY


@login_required(login_url='login')
def payment_checkout(request, transaction_id):
    user_transaction = get_object_or_404(Transaction, id=transaction_id)
    print("user_transaction :: ", user_transaction.total_spent)
    context = {
        "user_transaction": user_transaction
    }
    return render(request, 'paymentCheckout/payment_checkout.html', context)


def payment_successful(request):
    user_id = request.user.id
    transaction_id = request.session.get('transaction_id')
    user_object = User.objects.get(pk=user_id)
    user_payment = UserPayment.objects.create(user=user_object, payment_bool=True, transaction_id=transaction_id)
    if 'transaction_id' in request.session:
        del request.session['transaction_id']
    return render(request, 'paymentCheckout/payment_successful.html')


def payment_cancelled(request):
    return render(request, 'paymentCheckout/payment_cancelled.html')


class CreateCheckoutSession(View):
    def post(self, request, *args, **kwargs):
        currency = request.session.get('currency')
        YOUR_DOMAIN = 'http://127.0.0.1:8000/'
        transaction_id = request.POST.get('user_transaction')
        user_transaction = get_object_or_404(Transaction, id=transaction_id)
        product = stripe.Product.create(name=user_transaction.coin)
        total_spent = int(user_transaction.total_spent) * 100
        price = stripe.Price.create(
            unit_amount=total_spent,
            currency=currency,
            product=product.id,
        )
        print("price :: => ::", price)
        if 'transaction_id' in request.session:
            del request.session['transaction_id']
        request.session['transaction_id'] = transaction_id
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': price.id,
                        'quantity': 1,
                    }
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/payment_successful',
                cancel_url=YOUR_DOMAIN + '/payment_cancelled',
            )
        except Exception as e:
            return str(e)
        return redirect(checkout_session.url, code=303)
