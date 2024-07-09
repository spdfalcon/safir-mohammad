from django.contrib import admin
from .models import Ticket, Message, DefaultMessage

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
	list_display = ['user', 'title', 'priority', 'status', 'get_date_created', 'id']
	list_editable = ['status']
	list_filter = ['priority', 'status', 'user']
	search_fields = ['user__username', 'user__first_name', 'user__last_name', 'title']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
	list_display = ['ticket', 'admin_reply', 'is_seen', 'get_date_sent']
	list_filter = ['admin_reply', 'is_seen']
	search_fields = ['body', 'ticket__user__username', 'ticket__user__first_name', 'ticket__user__last_name']


@admin.register(DefaultMessage)
class DefaultMessage(admin.ModelAdmin):
	list_display = ['is_seen', 'get_date_sent']
	list_filter = ['is_seen']
	search_fields = ['body']