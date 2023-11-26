"""
URL configuration for CryptoNexa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from payments import views

urlpatterns = [
    path('checkout/<int:transaction_id>', views.payment_checkout, name='payment_checkout'),
    path('payment_successful', views.payment_successful, name='payment_successful'),
    path('payment_cancelled', views.payment_cancelled, name='payment_cancelled'),
    path('create-checkout-session', views.CreateCheckoutSession.as_view(), name='create-checkout-session'),
    path('payment_sell/<int:tran_id>', views.payment_sell, name='payment_sell'),
]
