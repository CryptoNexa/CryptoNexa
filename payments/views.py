import json
import time

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .forms import DirectDepositForm
from .models import UserPaymentBuy, UserPaymentSell
from django.views import View
from BuySell.models import Transaction
from django.shortcuts import get_object_or_404
from core.models import User
import stripe

# Create your views here.
stripe.api_key = settings.STRIPE_PRIVATE_KEY


@login_required(login_url='/login/')
def payment_checkout(request, transaction_id):
    user_transaction = get_object_or_404(Transaction, id=transaction_id)
    if user_transaction.type == "buy":
        print("user_transaction :: ", user_transaction.total_spent)
        context = {
            "user_transaction": user_transaction
        }
        return render(request, 'paymentCheckout/payment_checkout.html', context)
    else:
        print("sell")
        print("user_transaction :: ", user_transaction.total_spent)
        context = {
            "user_transaction": user_transaction
        }
        return redirect("payment_sell", tran_id=transaction_id)


@login_required(login_url='/login/')
def payment_successful(request):
    user_id = request.user.id
    transaction_id = request.session.get('transaction_id')
    stripe_id = request.session.get('stripe_id')
    user_object = User.objects.get(pk=user_id)
    transaction_obj = Transaction.objects.get(id=transaction_id)
    transaction_obj.status = "success"
    user_payment = UserPaymentBuy.objects.create(user=user_object, payment_status=True, transaction_id=transaction_obj,
                                                 stripe_id=stripe_id)
    transaction_obj.save()
    if 'transaction_id' in request.session:
        del request.session['transaction_id']

    context = {
        "user_payment": user_payment,
        "user_object": user_object,
        "transaction_obj": transaction_obj
    }
    return render(request, 'paymentCheckout/payment_successful.html', context)


@login_required(login_url='/login/')
def payment_cancelled(request):
    user_id = request.user.id
    transaction_id = request.session.get('transaction_id')
    print(transaction_id)
    transaction_obj = Transaction.objects.get(id=transaction_id)
    user_object = User.objects.get(pk=user_id)

    if transaction_obj.type == "buy":
        stripe_id = request.session.get('stripe_id')
        user_payment = UserPaymentBuy.objects.create(user=user_object, payment_status=False,
                                                     transaction_id=transaction_obj,
                                                     stripe_id=stripe_id)
    else:
        user_payment = UserPaymentSell.objects.create(user=user_object, payment_status=True,
                                                      transaction_id=transaction_obj,
                                                      account_holder_name="",
                                                      account_number=0,
                                                      transit_number=0,
                                                      routing_number=0, amount=0)

    context = {
        "user_payment": user_payment,
        "user_object": user_object,
        "transaction_obj": transaction_obj
    }

    transaction_obj.status = "failed"
    transaction_obj.save()
    return render(request, 'paymentCheckout/payment_cancelled.html', context)


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
                success_url=YOUR_DOMAIN + 'payment_successful',
                cancel_url=YOUR_DOMAIN + 'payment_cancelled',
            )
            request.session['stripe_id'] = checkout_session.id
            print("checkout_session :: => ::", checkout_session)
        except Exception as e:
            return str(e)
        return redirect(checkout_session.url, code=303)


@login_required(login_url='/login/')
def payment_sell(request, tran_id):
    try:
        user_transaction = get_object_or_404(Transaction, id=tran_id)
        request.session['transaction_id'] = tran_id
        initial_data = {"amount": user_transaction.total_spent}

        if request.method == "POST":
            user_id = request.user.id
            payment_sell_form = DirectDepositForm(request.POST)
            if payment_sell_form.is_valid():
                # raise Exception("known issue")
                account_holder_name = payment_sell_form.cleaned_data['account_holder_name']
                account_number = payment_sell_form.cleaned_data['account_number']
                transit_number = payment_sell_form.cleaned_data['transit_number']
                routing_number = payment_sell_form.cleaned_data['routing_number']
                amount = payment_sell_form.cleaned_data['amount']
                transaction_obj = Transaction.objects.get(id=tran_id)
                user_object = User.objects.get(pk=user_id)
                user_payment = UserPaymentSell.objects.create(user=user_object, payment_status=True,
                                                              transaction_id=transaction_obj,
                                                              account_holder_name=account_holder_name,
                                                              account_number=account_number,
                                                              transit_number=transit_number,
                                                              routing_number=routing_number, amount=amount)
                transaction_obj.status = Transaction.STATUS_CHOICES[1][0]
                transaction_obj.save()
                if 'transaction_id' in request.session:
                    del request.session['transaction_id']

                context = {
                    "user_payment": user_payment,
                    "user_object": user_object,
                    "transaction_obj": transaction_obj
                }
                return render(request, 'paymentCheckout/payment_successful.html', context)
            return render(request, 'paymentCheckout/payment_cancelled.html')
        else:
            payment_sell_form = DirectDepositForm(initial=initial_data)
        return render(request, "paymentCheckout/payment_sell_form.html", {"user_transaction": user_transaction,
                                                                          'form': payment_sell_form,
                                                                          'tran_id': tran_id})
    except Exception as e:
        print(e)
        return redirect('payment_cancelled')
