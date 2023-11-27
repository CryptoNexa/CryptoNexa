# update your main urls.py or create a new urls.py in the 'contact' app
from django.urls import path
from .views import contact_us_view , success_view

urlpatterns = [
    path('contact-us/', contact_us_view, name='contact-us'),
    path('contact-success/', success_view, name='contact-success'),

]
