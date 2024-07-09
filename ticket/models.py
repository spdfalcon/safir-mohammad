from django.db import models
from django_jalali.db import models as jmodels
from django.contrib.auth import get_user_model
from .utils import TICKET_PRIORITY_CHOICES, TICKET_STATUS_CHOICES
from .utils import MEDIUM, OPEN


User = get_user_model()

class Ticket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="کاربر", related_name='user_tickets')
    title = models.CharField(verbose_name="عنوان", max_length=50)
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)
    priority = models.CharField(verbose_name="اولویت", choices=TICKET_PRIORITY_CHOICES, \
                                default=MEDIUM, max_length=1)
    status = models.CharField(verbose_name="وضعیت", choices=TICKET_STATUS_CHOICES, \
                                default=OPEN, max_length=1)
    date_created = jmodels.jDateTimeField(verbose_name="تاریخ ایجاد", auto_now_add=True)
    index = models.PositiveBigIntegerField(verbose_name='ترتیب نمایش', null=True, blank=True)

    def get_date_created(self):
        return self.date_created.strftime("%Y/%m/%d ساعت %H:%M")
    get_date_created.short_description = 'تاریخ ایجاد'

    @property
    def get_priority(self):
        return dict(TICKET_PRIORITY_CHOICES)[self.priority]

    @get_priority.setter
    def get_priority(self, priority_type):
        reversed_types = {v: k for k, v in dict(TICKET_PRIORITY_CHOICES).items()}
        self.priority = reversed_types.get(priority_type)

    @property
    def get_status(self):
        return dict(TICKET_STATUS_CHOICES)[self.status]

    @get_status.setter
    def get_status(self, status_type):
        reversed_types = {v: k for k, v in dict(TICKET_STATUS_CHOICES).items()}
        self.status = reversed_types.get(status_type)

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} - {self.title}"
    

    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = '  تیکت‌ها'
        ordering = ('index', '-date_created', )



class Message(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, verbose_name="تیکت", related_name='messages')
    admin_reply = models.BooleanField(verbose_name="پاسخ ادمین", default=False)
    is_seen = models.BooleanField(verbose_name="خوانده‌شده", default=False)
    date_sent = jmodels.jDateTimeField(verbose_name="تاریخ ارسال", auto_now_add=True)
    body = models.TextField(verbose_name="متن پیام")

    def get_date_sent(self):
        return self.date_sent.strftime("%Y/%m/%d ساعت %H:%M")
    get_date_sent.short_description = 'تاریخ ارسال'

    def __str__(self) -> str:
        if self.admin_reply:
            return f"پیام مدیر در تاریخ {self.get_date_sent()}"
        return f"{self.ticket.user.get_full_name()} در تاریخ {self.get_date_sent()}"

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = ' پیام‌ها'
        ordering = ['date_sent']


class DefaultMessage(models.Model):
    is_seen = models.BooleanField(verbose_name="خوانده‌شده", default=False)
    date_sent = jmodels.jDateTimeField(verbose_name="تاریخ ارسال", auto_now_add=True)
    body = models.TextField(verbose_name="متن پیام")

    def get_date_sent(self):
        return self.date_sent.strftime("%Y/%m/%d ساعت %H:%M")
    get_date_sent.short_description = 'تاریخ ارسال'

    def __str__(self) -> str:
        return str(self.date_sent)

    class Meta:
        verbose_name = 'پیام پیشفرض'
        verbose_name_plural = 'پیام های پیشفرض'
        ordering = ('date_sent', )