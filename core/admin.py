from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from support.models import SupportIssue
from .models import User, Cryptocurrency, Quote, Watchlist, FooterList
from .forms import CustomUserForm, CustomUserChangeForm
from BuySell.models import Transaction
from payments.models import UserPaymentBuy
from payments.models import UserPaymentSell


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('date_joined',)

    add_form = CustomUserForm
    form = CustomUserChangeForm
    model = User

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'date_joined', 'photo_id'), 'classes': ('collapse',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('date_joined',)


# Register the CustomUser model with the admin site
admin.site.register(User, CustomUserAdmin)
admin.site.register(Cryptocurrency)
admin.site.register(Quote)
admin.site.register(Transaction)
admin.site.register(Watchlist)
admin.site.register(SupportIssue)
admin.site.register(UserPaymentSell)
admin.site.register(UserPaymentBuy)
admin.site.register(FooterList)
