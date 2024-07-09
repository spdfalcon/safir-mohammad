from django.contrib import admin
from .models import Wishlist, WishlistItem


class WishlistItemInline(admin.TabularInline):
    model = WishlistItem


@admin.register(Wishlist)
class Wishlist(admin.ModelAdmin):
    list_display = ('user', 'name', 'date_created', 'last_updated')
    inlines = [WishlistItemInline, ]
    
    