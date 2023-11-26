# forms.py
from django import forms
from .models import Currency


class SelectionForm(forms.Form):
    currencies = Currency.objects.all()
    choices = [(currency.code, f"{currency.name} ({currency.code})") for currency in currencies]

    selected_option = forms.ChoiceField(
        choices=choices,
        widget=forms.RadioSelect(attrs={'class': 'radio-select'}),
    )
