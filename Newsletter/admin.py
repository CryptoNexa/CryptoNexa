from django.contrib import admin
from .models import News, Subscriber

# Register your models here.
admin.site.register(News)
admin.site.register(Subscriber)