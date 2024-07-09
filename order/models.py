from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from jalali_date import date2jalali
from products.models import Package, Course, Part, Category
from django.urls import reverse
from main.utils import send_sms


User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_orders', verbose_name='کاربر')
    created_at = models.DateTimeField(verbose_name='تاریخ ایجاد', default=timezone.now)
    is_paid = models.BooleanField(default=False, verbose_name='پرداخت شده؟')
    paid_at = models.DateTimeField(verbose_name='تاریخ پرداخت', null=True, blank=True)
    price_after_discount = models.PositiveIntegerField(verbose_name='قیمت بعد از تخفیف', null=True, blank=True)
    ref_id = models.IntegerField(verbose_name="کد رهگیری پرداخت اینترنتی", blank=True, null=True)
    index = models.PositiveBigIntegerField(verbose_name='ترتیب نمایش', null=True, blank=True)

    class Meta:
        ordering = ('index', 'created_at', )
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'
    
    def __str__(self):
        return str(self.user.get_full_name()) + ' ' + str(self.get_created_at_jalali())
    
    @staticmethod
    def format_price_with_commas(price):
        return '{:,.0f}'.format(price)

    def formatted_price(self):
        return self.format_price_with_commas(self.get_price())

    def formatted_price_after_discount(self):
        return self.format_price_with_commas(self.get_price_after_discount())

    def formatted_price_minus_discount(self):
        return self.format_price_with_commas(self.get_price_minus_discount())
    
    def get_price(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_price_after_discount(self):
        if self.price_after_discount:
            return self.price_after_discount
        return self.get_price()
    
    def get_price_minus_discount(self):
        return self.get_price() - self.get_price_after_discount()
    
    def get_is_paid(self):
        if self.is_paid:
            return 'پرداخت شده'
        return 'پرداخت نشده'
    
    def get_created_at_jalali(self):
        if self.created_at is not None:  
            return date2jalali(self.created_at).strftime('%Y/%m/%d')
        else:
            return ''
        
    def get_paid_at_jalali(self):
        if self.paid_at is not None:  
            return date2jalali(self.paid_at).strftime('%Y/%m/%d')
        else:
            return ''
        
    def get_item_titles(self):
        item_titles = []
        for item in self.items.all():
            item_titles.append(item.get_title())
        return '، '.join(item_titles)
    
    def send_sms_for_items_less_than_15_days(self):
        for item in self.items.all():
            item.send_sms_if_remaining_days_less_than_15()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="سفارش مربوطه")
    package = models.ForeignKey(Package, related_name='order_items', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="دسته بندی مربوطه")
    course = models.ForeignKey(Course, related_name='order_items', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="مجموعه مربوطه")
    part = models.ForeignKey(Part, related_name='order_items', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="محصول مربوطه")
    price = models.PositiveIntegerField(verbose_name="قیمت")

    class Meta:
        verbose_name = "آیتم"
        verbose_name_plural = "آیتم ها"
  
    
    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price
        
    def get_title(self):
        if self.package:
            return self.package.title
        elif self.course:
            return self.course.title
        elif self.part:
            return self.part.title
        else: 
            return ''
    
    def get_image_url(self):
        if self.package:
            return self.package.image.url
        elif self.course:
            return self.course.image.url
        
        return self.part.image.url
    
    def get_detail_url(self):
        if self.package:
            return reverse('edu:package_detail', kwargs={'package_slug': self.package.slug})
        elif self.course:
            return reverse('edu:course_detail', kwargs={'course_slug': self.course.slug})
        else:
            return reverse('edu:part_detail', kwargs={'part_slug': self.part.slug})
        
    
    def send_sms_if_remaining_days_less_than_15(self):
        remaining_days = self.calculate_remaining_days()
        if remaining_days is not None and remaining_days <= 15:
            user = self.order.user
            phone = user.profile.phone  # Assuming user has a profile with phone field
            
            # Send SMS notification
            message = f"Your time is less than 15 days for {self.get_title()}"
            data = {
                "receptor": phone,
                "token": message,
                "template": 'safir-login'
            }
            send_sms(data, 'phone_verify', user)

    def calculate_remaining_days(self):
        if self.package:
            return self.calculate_remaining_days_for_package()
        elif self.course:
            return self.calculate_remaining_days_for_course()
        return None

    def calculate_remaining_days_for_package(self):
        if self.order.paid_at is not None:
            end_date = self.order.paid_at.date() + timezone.timedelta(days=self.package.day_limit)
            return (end_date - timezone.now().date()).days
        return None

    def calculate_remaining_days_for_course(self):
        if self.order.paid_at is not None:
            end_date = self.order.paid_at.date() + timezone.timedelta(days=self.course.day_limit)
            return (end_date - timezone.now().date()).days
        return None


class Discount(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='کد تخفیف')
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='مقدار تخفیف')
    is_active = models.BooleanField(default=True, verbose_name='فعال بودن')
    start_date = models.DateTimeField(verbose_name='تاریخ شروع')
    end_date = models.DateTimeField(verbose_name='تاریخ پایان')
    user = models.ManyToManyField(User, related_name='user_discounts', verbose_name='کاربر', blank=True)
    order = models.ManyToManyField(Order, related_name='order_discounts', verbose_name='سفارش', blank=True)
    index = models.PositiveBigIntegerField(verbose_name='ترتیب نمایش', null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='discounts', null=True, blank=True)

    class Meta:
        verbose_name = 'تخفیف'
        verbose_name_plural = 'تخفیف‌ها'
        ordering = ('index', )

    def __str__(self):
        return f'{self.code} - {self.get_is_valid()}'
    
    def check_is_valid(self):
        now = timezone.now()
        return self.is_active and self.start_date <= now and self.end_date >= now

    def get_is_valid(self):
        if self.check_is_valid():
            return 'فعال'
        return 'غیرفعال'

    def apply_discount(self, order):
        if self.check_is_valid():
            return order.get_price() - self.value   
        return 0
    
    def get_start_date_jalali(self):
        if self.start_date is not None:  
            return date2jalali(self.start_date).strftime('%Y/%m/%d')
        else:
            return ''
        
    def get_end_date_jalali(self):
        if self.end_date is not None:  
            return date2jalali(self.end_date).strftime('%Y/%m/%d')
        else:
            return ''

    @staticmethod
    def check_discount_for_correct_category(discount, order):
        order_items = order.items.all()
        discount_category_list = [dis.title for dis in discount.categories.all()]

        category_title_list = []
        for item in order_items:
            if item.package:
                categories = item.package.categories.all()
                for category in categories:
                    category_title_list.append(category.title)

            if item.course:
                categories = item.course.categories.all()
                for category in categories:
                    category_title_list.append(category.title)

            if item.part:
                category = item.part.category
                category_title_list.append(category.title)

        for category in discount_category_list:
            if category in category_title_list:
                return True
        return False
