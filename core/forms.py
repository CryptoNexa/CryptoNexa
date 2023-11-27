from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Watchlist, Cryptocurrency


class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'photo_id']  # Add custom fields as needed


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'photo_id']  # Add custom fields as needed


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'photo_id']


class WatchlistForm(forms.ModelForm):
    cryptocurrencies = forms.ModelMultipleChoiceField(
        queryset=Cryptocurrency.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Select Cryptocurrencies',
        required=False
    )

    class Meta:
        model = Watchlist
        fields = ['name', 'cryptocurrencies']
        widgets = {
            'name': forms.TextInput(attrs={'required': False}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        model = User  # Use the User model from Django's auth module
        fields = ['first_name', 'last_name', 'email']


class CurrencyConverterForm(forms.Form):
    amount = forms.DecimalField(label='Amount', min_value=1e-8, max_value=1000000000000, initial=1)
    base_currency = forms.CharField(label='Base Currency', max_length=100)
    convert_currency = forms.CharField(label='Convert To', max_length=100)
