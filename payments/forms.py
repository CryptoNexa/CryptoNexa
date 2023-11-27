# forms.py
from django import forms
from .models import UserPaymentSell

class DirectDepositForm(forms.ModelForm):
    class Meta:
        model = UserPaymentSell
        fields = ['account_holder_name', 'account_number', 'transit_number', 'routing_number', 'amount']
        widgets = {
            'account_holder_name': forms.TextInput(attrs={'class': 'form-control '}),
            'account_number': forms.NumberInput(attrs={'class': 'form-control '}),
            'transit_number': forms.NumberInput(attrs={'class': 'form-control '}),
            'routing_number': forms.NumberInput(attrs={'class': 'form-control '}),
            'amount': forms.NumberInput(attrs={'class': 'form-control '}),
        }