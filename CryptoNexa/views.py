# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render


def index(request):
    return render(request, 'CryptoNexa/index.html')
