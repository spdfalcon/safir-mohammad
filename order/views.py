from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from panel.models import MinimumCartCost
from .models import Order, OrderItem, Discount
from products.models import Package, Course, Part
from cart.cart import Cart


class OrderCreateView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        cart = Cart(request)

        mcc = MinimumCartCost.objects.first()
        
        if mcc and cart.get_total_price() < mcc.minimum_cart_cost:
            messages.error(request, f'حداقل مبلغ سفارش باید بیشتر از {mcc.minimum_cart_cost} باشد')
            return redirect('main:home')
        
        order = Order.objects.create(user=request.user)


        for item in cart:
            package, course, part = [None, None, None]
            if item['product_type'] == 'package':
                package = get_object_or_404(Package, id=item['product_id'])
            elif item['product_type'] == 'course':
                course = get_object_or_404(Course, id=item['product_id'])
            else:
                part = get_object_or_404(Part, id=item['product_id'])

            OrderItem.objects.create(order=order,
                                     package=package, 
                                     course=course,
                                     part=part,
                                     price=item['price'])
            
        cart.clear()
        request.session['order_id'] = order.id
        return redirect("order:order_process")

class OrderProcessView(LoginRequiredMixin, View):
    template_name = 'order/order_process.html'

    def get(self, request, *args, **kwargs):
        order_id = request.session.get('order_id')
        discount_code = request.GET.get('discount_code')

        if not order_id:
            messages.error(request, "سفارش وجود ندارد")
            return render(request, 'error_pages/page_404.html')
            
        order = get_object_or_404(Order, id=order_id)
        if discount_code:
            try:
                discount = Discount.objects.get(code=discount_code)
            except Discount.DoesNotExist:
                messages.error(request, "کد تخفیف وجود ندارد.")
                return redirect('order:order_process')  
            
            if not discount.check_is_valid():
                messages.error(request, "کد تخفیف منقضی شده است.")
                return redirect('order:order_process')  

            if not discount.check_discount_for_correct_category(discount, order):
                messages.error(request, 'کد تخفیف برای این دسته از محصولات تعریف نشده است.')
                return redirect('order:order_process')

            # Apply discount to order
            order.price_after_discount = discount.apply_discount(order)
            order.save()
            discount.order.add(order)
            messages.success(request, "تخفیف اعمال گردید.")

        return render(request, self.template_name, {'order': order})
