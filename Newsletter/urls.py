from django.urls import path
from .views import news_list, subscribe, success_view

urlpatterns = [
    path('news/', news_list, name='news_list'),
    path('news/subscribe/', subscribe, name='subscribe'),
    path('success/', success_view, name='success')
]
