from django import forms

# Choices for greater than or less than
GT_LT_CHOICES = [
    ('gt', 'Greater Than'),
    ('lt', 'Less Than'),
]

INFINITE_SUPPLY_CHOICES = [
    (True, 'Yes'),
    (False, 'No'),
]


class CryptoFilterForm(forms.Form):
    name = forms.CharField(required=False, label='Name', max_length=50, widget=forms.TextInput(attrs={'class': 'custom-input'}))
    num_market_pairs = forms.IntegerField(required=False, label='Number of Market Pairs',
                                          widget=forms.NumberInput(attrs={'class': 'custom-input'}))
    circulating_supply = forms.DecimalField(required=False, label='Circulating Supply', max_digits=20, decimal_places=2,
                                            widget=forms.NumberInput(attrs={'class': 'custom-input'}))
    total_supply = forms.DecimalField(required=False, label='Total Supply', max_digits=20, decimal_places=2,
                                      widget=forms.NumberInput(attrs={'class': 'custom-input'}))
    max_supply = forms.DecimalField(required=False, label='Max Supply', max_digits=20, decimal_places=2,
                                    widget=forms.NumberInput(attrs={'class': 'custom-input'}))
    infinite_supply = forms.ChoiceField(required=False, label='Infinite Supply', choices=INFINITE_SUPPLY_CHOICES,
                                       widget=forms.RadioSelect(attrs={'class': 'custom-input-radio'}))

    """Quote Related"""
    price_min = forms.DecimalField(required=False, label='Min Price', max_digits=20, decimal_places=2,
                               widget=forms.NumberInput(attrs={'class': 'custom-input'}))
    price_max = forms.DecimalField(required=False, label='Max Price', max_digits=20, decimal_places=2,
                               widget=forms.NumberInput(attrs={'class': 'custom-input'}))

    def clean(self):
        cleaned_data = super().clean()
        price_min = cleaned_data.get('price_min')
        price_max = cleaned_data.get('price_max')

        if price_min is not None and price_max is not None and price_min > price_max:
            raise forms.ValidationError('Min Price cannot be greater than Max Price.')

        return cleaned_data
