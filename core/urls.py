from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'core'

urlpatterns = [
    path('register/', csrf_exempt(views.register), name='register'),
    path('login/', csrf_exempt(views.user_login), name='login'),
    path('logout/', csrf_exempt(views.user_logout), name='logout'),
    path('profile/<int:id>', csrf_exempt(views.user_profile), name='profile'),
    path('edit_profile/<int:id>', csrf_exempt(views.user_edit_profile), name='edit_profile'),
    path('crypto/<slug:slug>/', views.crypto_detail, name='crypto_detail'),
    path('get_updated_crypto_data/<int:fetch_live_data>', views.get_updated_crypto_data,
         name='get_updated_crypto_data'),
    path('watchlist/', csrf_exempt(views.watchlist), name='watchlist'),
    path('watchlist/<int:watchlist_id>/', views.watchlist, name='watchlist'),
    path('create_watchlist/', csrf_exempt(views.create_watchlist), name='create_watchlist'),
    path('edit_watchlist_name/<int:watchlist_id>/', csrf_exempt(views.edit_watchlist_name), name='edit_watchlist_name'),
    path('payment_history/', csrf_exempt(views.payment_history), name='payment_history'),
    path('payment_history/',csrf_exempt(views.payment_history),name='payment_history'),
    path('currency_converter/',csrf_exempt(views.currency_converter), name='currency_converter')

    # Add other URL patterns as needed for your application
]
