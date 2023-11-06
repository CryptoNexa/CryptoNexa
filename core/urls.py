from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [

    path('register/', csrf_exempt(views.register), name='register'),
    path('login/', csrf_exempt(views.user_login), name='login'),
    path('logout/', csrf_exempt(views.user_logout), name='logout'),
    path('profile/<int:id>', csrf_exempt(views.user_profile), name='profile'),
    path('edit_profile/<int:id>', csrf_exempt(views.user_edit_profile), name='edit_profile'),
    # Add other URL patterns as needed for your application
]
