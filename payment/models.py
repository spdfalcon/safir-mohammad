from django.db import models
from main.models import General
from django.utils import timezone
from order.models import Order
from accounts.models import User


class PaymentSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=100, verbose_name='نوع')

    def is_expired(self):
        # Define a timeout for session validity (e.g., 1 hour)
        return self.created_at < timezone.now() - timezone.timedelta(hours=1)

        
    
class PaymentHistory(General):
    user = models.ForeignKey('accounts.User', null=True, on_delete=models.SET_NULL)
    card_number = models.CharField(max_length=128, null=True, blank=True)
    ref_number = models.CharField(max_length=128, null=True, blank=True)
    invoice_number = models.CharField(max_length=128, null=True, blank=True)
    message = models.CharField(max_length=225, null=True, blank=True)
    amount = models.PositiveIntegerField(default=0)
    package = models.ForeignKey('products.Package', \
                                       null=True, blank=True, on_delete=models.SET_NULL)
    course = models.ForeignKey('products.Course', \
                                       null=True, blank=True, on_delete=models.SET_NULL)
    is_success = models.BooleanField(default=False)
    verified_before = models.BooleanField(default=False)
    

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'تاریخچه پرداخت'
        verbose_name_plural = 'تاریخچه پرداخت ها'

    
    def __str__(self):
        return 
    
class WalletAmountSession(General):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    amount = models.IntegerField(default=0, verbose_name='مقدار')
    type = models.CharField(max_length=100, verbose_name='نوع')
    description = models.TextField(verbose_name='توضیحات')


    