from django.db import models
from main.models import General


class NotificationLog(General):
    STATUS = (
                ('success', 'موفق'),
                ('failure', 'ناموفق')
            )
    title = models.CharField(max_length=200, verbose_name='عنوان')
    body = models.TextField(verbose_name='محتوا')
    link = models.URLField(max_length=400, verbose_name='لینک ریدایرکت')
    status = models.CharField(max_length=100, choices=STATUS, verbose_name='وضعیت ارسال')
    
    class Meta:
        verbose_name = 'تاریخچه نوتیفیکیشن ها'
        verbose_name_plural = 'تاریخچه نوتیفیکیشن ها'

    
    def __str__(self):
        return self.title + str(self.get_created_at)
    

class MinimumCartCost(General):
    minimum_cart_cost = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f'{self.minimum_cart_cost}'

    def format_price_with_commas(self):
        return '{:,.0f}'.format(self.minimum_cart_cost)
