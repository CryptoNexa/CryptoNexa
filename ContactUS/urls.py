# update your main urls.py or create a new urls.py in the 'contact' app
from django.urls import path
from .views import contact_us_view , success_view

urlpatterns = [
    path('Contact_us/', contact_us_view, name='contact-us'),
    path('Contact-success/', success_view, name='ContactUs/success'),
    # Other URL patterns...
]
