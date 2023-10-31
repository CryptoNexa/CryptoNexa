from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']  # Add custom fields as needed

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']  # Add custom fields as needed

