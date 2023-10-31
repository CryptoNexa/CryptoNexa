
from django.urls import path
from . import views

urlpatterns = [
    path('crypto_list_view/', views.crypto_list_view, name='crypto_list_view'),
]