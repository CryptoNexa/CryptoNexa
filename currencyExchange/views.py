from django.shortcuts import render, redirect

from .forms import SelectionForm
from .models import Currency


# Create your views here.
def currency_exchange(request):
    currencies = Currency.objects.all()

    if request.method == 'POST':
        form = SelectionForm(request.POST)
        if form.is_valid():
            selected_option = form.cleaned_data['selected_option']
            request.session['currency'] = selected_option
            return redirect('/')  # Redirect to the previous page or a default page.
    else:
        form = SelectionForm()

    context = {
        "currencies": currencies,
        "form": form
    }
    return render(request, 'currencyExchange/currency_exchange_view.html', context)


def redirect_to_previous(request):
    return redirect(request.META.get('HTTP_REFERER'))
