from django import forms

from BuySell.models import Transaction
from datetime import datetime


class TransactionForm(forms.ModelForm):
    TRANSACTION_TYPES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    ]
    COIN_TYPES = [
        ('bitcoin', "Bitcoin BTC"),
        ('ethereum', "Ethereum ETH"),
    ]
    default_format = '%b. %d, %Y, %I:%M %p'

    type = forms.ChoiceField(choices=TRANSACTION_TYPES, widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
                             initial="buy")
    coin = forms.CharField(label="Coin")
    price = forms.DecimalField()
    datetime = forms.DateTimeField(
        input_formats=['%b. %d, %Y, %I:%M %p'],  # Format used in your example
        widget=forms.TextInput(attrs={'id': 'id_datetime'}),  # Use the same ID as in your example
        initial=datetime.now().strftime(default_format)
    )

    class Meta:
        model = Transaction
        fields = ['type', 'coin', 'quantity', 'price', 'datetime', 'transaction_fee', 'notes', 'total_spent']
