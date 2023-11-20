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
    # price = forms.DecimalField(required=False, label='Price', max_digits=20, decimal_places=2,
    #                            widget=forms.NumberInput(attrs={'class': 'custom-input'}))
    # price_gt_or_lt = forms.ChoiceField(required=False, label='Price Greater Than or Less Than', choices=GT_LT_CHOICES,
    #                                    widget=forms.RadioSelect(attrs={'class': 'custom-input-radio'}))
    # percent_change_1h = forms.DecimalField(required=False, label='Percent Change (1h)', max_digits=20, decimal_places=2,
    #                                        widget=forms.NumberInput(attrs={'class': 'custom-input'}))
    # percent_change_1h_gt_or_lt = forms.ChoiceField(required=False, label='Percent Change (1h) Greater Than or Less Than',
    #                                                choices=GT_LT_CHOICES,
    #                                                widget=forms.RadioSelect(attrs={'class': 'custom-input-radio'}))
    # percent_change_24h = forms.DecimalField(required=False, label='Percent Change (24h)', max_digits=20, decimal_places=2,
    #                                         widget=forms.NumberInput(attrs={'class': 'custom-input'}))
    # percent_change_24h_gt_or_lt = forms.ChoiceField(required=False, label='Percent Change (24h) Greater Than or Less Than',
    #                                                 choices=GT_LT_CHOICES,
    #                                                 widget=forms.RadioSelect(attrs={'class': 'custom-input-radio'}))
    # market_cap = forms.DecimalField(required=False, label='Market Cap', max_digits=20, decimal_places=2,
    #                                 widget=forms.NumberInput(attrs={'class': 'custom-input'}))
    # market_cap_gt_or_lt = forms.ChoiceField(required=False, label='Market Cap Greater Than or Less Than', choices=GT_LT_CHOICES,
    #                                         widget=forms.RadioSelect(attrs={'class': 'custom-input-radio'}))
    # volume_24h = forms.DecimalField(required=False, label='Volume (24h)', max_digits=20, decimal_places=2,
    #                                 widget=forms.NumberInput(attrs={'class': 'custom-input'}))
    # volume_24h_gt_or_lt = forms.ChoiceField(required=False, label='Volume (24h) Greater Than or Less Than', choices=GT_LT_CHOICES,
    #                                         widget=forms.RadioSelect(attrs={'class': 'custom-input-radio'}))
