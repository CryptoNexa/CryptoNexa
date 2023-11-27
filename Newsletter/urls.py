from django.urls import path
from .views import news_list, subscribe, success_view

urlpatterns = [
    path('news_list/', news_list, name='news_list'),
    path('subscribe/', subscribe, name='subscribe'),
    path('success/', success_view, name='success')
]
