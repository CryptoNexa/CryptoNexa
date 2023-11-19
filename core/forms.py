from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Watchlist, Cryptocurrency


class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']  # Add custom fields as needed


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']  # Add custom fields as needed


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User  # Use the User model from Django's auth module
        fields = ['first_name', 'last_name', 'email']

class WatchlistForm(forms.ModelForm):
    cryptocurrencies = forms.ModelMultipleChoiceField(
        queryset=Cryptocurrency.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Select Cryptocurrencies',
        required=False
    )

    class Meta:
        model = Watchlist
        fields = ['cryptocurrencies']