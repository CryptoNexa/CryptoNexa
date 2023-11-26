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
