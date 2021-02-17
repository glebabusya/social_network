from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import AccountCreationForm, AccountChangeForm
from .models import Account


class AccountAdmin(UserAdmin):
    add_form = AccountCreationForm
    form = AccountChangeForm
    model = Account

    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)

    fieldsets = (
        (None, {'fields': ('email', 'password', 'username', 'gender', 'first_name', 'last_name', 'phone_number',
                           'birthday', 'avatar', 'work', 'study', 'city', 'current_info', 'time_join', 'can_comment',
                           'closed', 'banned')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(Account, AccountAdmin)
