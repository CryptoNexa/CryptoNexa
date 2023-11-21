from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [

    path('buysell/<str:slug>/<str:name>/<str:price>/', csrf_exempt(views.buysell), name='buysell'),
    path('currency/', csrf_exempt(views.currency), name='currency'),
    # Add other URL patterns as needed for your application
]
