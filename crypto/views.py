from django.shortcuts import render

# Create your views here.


def crypto_list_view(request):
    return render(request, 'crypto/crypto_list_view.html', {})