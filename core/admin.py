from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from BuySell.models import Transaction


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('date_joined',)


# Register the CustomUser model with the admin site
admin.site.register(User, CustomUserAdmin)
admin.site.register(Transaction)
