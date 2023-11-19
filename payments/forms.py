# forms.py
from django import forms
from .models import UserPaymentSell

class DirectDepositForm(forms.ModelForm):
    class Meta:
        model = UserPaymentSell
        fields = ['account_holder_name', 'account_number', 'transit_number', 'routing_number', 'amount']