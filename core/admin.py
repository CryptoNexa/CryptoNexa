from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Cryptocurrency, Quote
from .models import User
from BuySell.models import Transaction
from payments.models import UserPayment


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('date_joined',)


# Register the CustomUser model with the admin site
admin.site.register(User, CustomUserAdmin)
admin.site.register(Cryptocurrency)
admin.site.register(Quote)
admin.site.register(Transaction)
admin.site.register(UserPayment)
