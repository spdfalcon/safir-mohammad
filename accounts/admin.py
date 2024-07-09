from django.contrib import admin
from django.contrib import admin
from django.contrib.admin.decorators import register
from django.contrib.auth.admin import UserAdmin as AbstractUserAdmin
from .models import *
from django.contrib.auth.models import Group


# ----------------------------- Unregister Group ---------------------------
admin.site.unregister(Group)
admin.site.register(Wallet)

# ----------------------------- User ---------------------------------------
@register(User)
class UserAdmin(AbstractUserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'phone',
                    'get_date_joined', 'get_last_update', 'is_active', 'is_superuser']

    list_filter = ['is_active', 'is_superuser']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    readonly_fields = ['get_date_joined', 'get_last_update', 'get_last_login']
    list_display_links = ['username']

    fieldsets = (
        ('اطلاعات ورود', {
            'fields': ('username', 'password')
        }),

        ('اطلاعات شخصی', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),

        ('دسترسی‌ها', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'dashboards',
                'user_permissions',
            )
        }),

        ('تاریخ‌های مهم', {'fields': ('get_date_joined',
                                      'get_last_update', 'get_last_login')})
    )

    add_fieldsets = (
        ('اطلاعات ورود', {
            'fields': ('username', 'password1', 'password2')
        }),

        ('اطلاعات شخصی', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),

        ('دسترسی‌ها', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'dashboards',
                'user_permissions',
            )
        })
    )
# ----------------------------- Verify Code ---------------------------------------
@register(VerificationCode)
class VerifyCodeAdmin(admin.ModelAdmin):
    list_display = ("user", "subject" ,"code" ,"attempts" ,"status", "get_created_at")
    list_filter = ("user", "status", "subject", "created_at")
    search_fields = ("code", )
    readonly_fields = ('code', )


@admin.register(TransactionHistory)
class TransactionHistoryAdmin(admin.ModelAdmin):
    list_display = ['wallet', 'amount', 'transaction_type', 'charge_by', 'message']
