from django import forms
from .models import Subscriber


class Subscription(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']

    def save(self, commit=True):
        instance = super(Subscription, self).save(commit=False)
        if commit:
            instance.save()
        return instance
