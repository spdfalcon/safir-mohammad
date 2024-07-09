from django.shortcuts import render, redirect
from products.models import Package, Course, Part
from .cart import Cart  
from django.http import HttpResponseRedirect
from django.contrib import messages


def item_add(request, id):
    package, course, part = [None, None, None]
    cart = Cart(request)
    product_type = request.GET.get('product_type') 
    
    if product_type == 'package':
        package = Package.objects.get(id=id)
    elif product_type == 'course':
        course = Course.objects.get(id=id)
    else:
        part = Part.objects.get(id=id)

    if package:
        product_id = package.id
        product_title = package.title
    elif course:
        product_id = course.id
        product_title = course.title
    else:
        product_id = part.id
        product_title = part.title

    cart.add(product_id=product_id, product_type=product_type, quantity=1)
    messages.success(request, f' {product_title} به سبد خرید شما اضافه شد ')

    # Redirect back to the previous page or a specified URL
    if request.GET.get('next'):
        return redirect(request.GET['next'])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def item_clear(request, id, product_type):
    cart = Cart(request)
    package, course, part = [None, None, None]
    print(product_type)
    if product_type == 'package':
        package = Package.objects.get(id=id)
        product_id = package.id
        product_title = package.title
    elif product_type == 'course':
        course = Course.objects.get(id=id)
        product_id = course.id
        product_title = course.title
    else:
        part = Part.objects.get(id=id)
        product_id = part.id
        product_title = part.title

    cart.remove(product_id)
    messages.success(request, f'{product_title} از سبد خرید شما حذف شد')

    # Redirect back to the previous page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    messages.success(request, "سبد خرید با موفقیت خالی شد.")
    return redirect("cart:cart_detail")

def cart_detail(request):
    return render(request, 'cart/cart_detail.html')