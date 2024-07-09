from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Wishlist, WishlistItem
from products.models import Package, Course, Part
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


# ----------------------- show wishlist products ----------------------
class WishListView(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        wishlist = Wishlist.objects.filter(user=request.user).last()
        return render(request, 'profiles/wishlist.html', {'wishlist': wishlist})
    
# ----------------------- add product to wishlist ----------------------
class WishListAddView(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        package, course, part = [None, None, None]
        package_id = kwargs.get('package_id', None)
        course_id = kwargs.get('course_id', None)
        part_id = kwargs.get('part_id', None)

        if package_id:
            package = get_object_or_404(Package, id=package_id)
        elif course_id:
            course = get_object_or_404(Course, id=course_id)
        else:
            part = get_object_or_404(Part, id=part_id)

        wishlist = Wishlist.objects.filter(user=request.user).last()
        if wishlist is None:
            wishlist = Wishlist.objects.create(user=request.user, name='new_wishlist')
        
        if package:
            wishlist.add_package(package)
        elif course:
            wishlist.add_course(course)
        elif part:
            wishlist.add_part(part)
            
        messages.success(request, 'به لیست علاقه مندی ها افزوده شد')
        return redirect('wishlist:wishlist')
    
    
# ----------------------- delete product to wishlist ----------------------
class WishListDeleteView(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        wishlist = Wishlist.objects.filter(user=request.user).last()
        wishlist.delete_item(kwargs['item_id'])
        messages.error(request, 'محصول از لیست علاقه مندی ها حذف شد')
        return redirect('wishlist:wishlist')