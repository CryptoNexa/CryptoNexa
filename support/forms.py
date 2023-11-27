# forms.py
from django import forms

from BuySell.models import Transaction
from .models import SupportIssue


class SupportForm(forms.ModelForm):
    class Meta:
        model = SupportIssue
        fields = ['issue_type', 'issue_title', 'issue_description', 'transaction_id', 'files']

    files = forms.FileField(widget=forms.FileInput, required=False)
    # files = MultiFileField(min_num=0, max_num=10, max_file_size=1024*1024*5)

    def __init__(self, *args, user=None, **kwargs):
        super(SupportForm, self).__init__(*args, **kwargs)
        # Get transactions for the user
        transactions = Transaction.objects.filter(user=user)

        # Customize the choices for the transaction_id field
        choices = [('', '----')]  # Default option
        if transactions.exists():
            choices += [(transaction.id, transaction.id) for transaction in transactions]

        self.fields['transaction_id'].choices = choices