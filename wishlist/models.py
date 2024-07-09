"""
Copyright (c) 2023 - present Sdata.ir|Hamed Mirzaei|HamedMirzaei2001Official@gmail.com
"""

from django.db import models
from core.settings import AUTH_USER_MODEL
from products.models import Package, Course, Part


class Wishlist(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlists')
    name = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'لیست علاقه مندی'
        verbose_name_plural = 'لیست های علاقه مندی'

    def add_part(self, part):
        """
        Adds the exact part to this wishlist, if it is not already there.
        """
        items = WishlistItem.objects.filter(wishlist=self, part=part)
        if not items.exists():
            item = WishlistItem.objects.create(wishlist=self, part=part)
            item.save()
        self.save() # to get the last updated timestamp for this wishlist


    def add_course(self, course):
        """
        Adds the exact course to this wishlist, if it is not already there.
        """
        items = WishlistItem.objects.filter(wishlist=self, course=course)
        if not items.exists():
            item = WishlistItem.objects.create(wishlist=self, course=course)
            item.save()
        self.save() # to get the last updated timestamp for this wishlist

    def add_package(self, package):
        """
        Adds the exact package to this wishlist, if it is not already there.
        """
        items = WishlistItem.objects.filter(wishlist=self, package=package)
        if not items.exists():
            item = WishlistItem.objects.create(wishlist=self, package=package)
            item.save()
        self.save() # to get the last updated timestamp for this wishlist


    def get_all_items(self):
        """
        Return all items of this wishlist
        """
        return WishlistItem.objects.filter(wishlist=self)
        
    def find_item(self, product):
        """
        For a given product, find an entry in this wishlist 
        and return the found WishlistItem or None.
        """
        try:
            return WishlistItem.objects.get(wishlist=self, course=product) or WishlistItem.objects.get(wishlist=self, package=product) or \
                WishlistItem.objects.get(Wishlist=self, part=product)
        
        except WishlistItem.DoesNotExist:
            return None

    def delete_item(self, item_id):
        """
        A simple convenience method to delete an item from the wishlist.
        """
        WishlistItem.objects.get(pk=item_id).delete()
        self.save()


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='items', blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='items', blank=True, null=True)
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='items', blank=True, null=True)


    class Meta:
        verbose_name = 'ایتم'
        verbose_name_plural = 'ایتم ها'