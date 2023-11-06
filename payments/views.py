import json
import time

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import UserPayment
from django.views import View
import stripe

# Create your views here.
stripe.api_key = settings.STRIPE_PRIVATE_KEY


@login_required(login_url='login')
def payment_checkout(request):
    return render(request, 'paymentCheckout/payment_checkout.html')


def payment_successful(request):
    # checkout_session_id = request.GET.get('session_id', None)
    # session = stripe.checkout.Session.retrieve(checkout_session_id)
    # customer = stripe.Customer.retrieve(session.customer)
    # user_id = request.user
    # user_payment = UserPayment.objects.get(user=user_id)
    # user_payment.stripe_checkout_id = checkout_session_id
    # user_payment.save()
    return render(request, 'paymentCheckout/payment_successful.html')


def payment_cancelled(request):
    return render(request, 'paymentCheckout/payment_cancelled.html')


class CreateCheckoutSession(View):
    def post(self, request, *args, **kwargs):
        currency = request.session.get('currency')
        YOUR_DOMAIN = 'http://127.0.0.1:8000/'
        product = stripe.Product.create(name="test-1")
        price = stripe.Price.create(
            unit_amount=20000,
            currency=currency,
            product=product.id,
        )
        print("price :: => ::", price)
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': price.id,
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/payment_successful',
                cancel_url=YOUR_DOMAIN + '/payment_cancelled',
            )
        except Exception as e:
            return str(e)
        return redirect(checkout_session.url, code=303)
