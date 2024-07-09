from django.contrib import admin
from .models import *



class ReadOnlyAdmin(admin.ModelAdmin):
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields] + \
               [field.name for field in obj._meta.many_to_many]


    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(SmsLog)
class SmsLogAdmin(ReadOnlyAdmin):
    list_display = ('user', 'subject', 'is_sent', 'status_code', 'get_created_at')
    list_filter = ('user', 'subject', 'is_sent', 'status_code', 'created_at')
    ordering = ('-created_at', )
    readonly_fields = ('status_code_str', )



@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Dashboard._meta.fields if field.name not in ["id"]]
    search_fields = [field.name for field in Dashboard._meta.fields if field.name not in ["id"]]


admin.site.register(LoginPage)
admin.site.register(WebSites)