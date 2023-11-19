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

    # Crypto Related URLs
    path('crypto/<slug:slug>/', views.crypto_detail, name='crypto_detail'),
    path('get_updated_crypto_data/<int:fetch_live_data>', views.get_updated_crypto_data, name='get_updated_crypto_data'),
]
