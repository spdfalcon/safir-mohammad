from enum import Enum
from django.db import models
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from main.models import General
from django.db.models import Q
from jalali_date import datetime2jalali, date2jalali
from datetime import datetime
from .managers import UserManager
from .utils import generate_new_verification_code
from main.models import Dashboard



class User(AbstractUser):
    first_name = models.CharField(verbose_name="نام", max_length=30, default='')
    last_name = models.CharField(verbose_name="نام خانوادگی", max_length=50, default='')
    date_joined = models.DateTimeField(verbose_name="تاریخ عضویت", null=True, blank=True, default=datetime.now)
    last_update = models.DateTimeField(verbose_name="آخرین بروزرسانی", auto_now=True, null=True)
    last_login = models.DateTimeField(verbose_name="آخرین ورود", null=True, blank=True)
    phone = models.CharField(verbose_name="تلفن همراه", null=True, max_length=11, unique=True)
    email = models.EmailField(verbose_name="ایمیل", null=True, blank=True)
    valid_phone = models.BooleanField(default=False, verbose_name="تایید تلفن همره")    
    valid_email = models.BooleanField(default=False, verbose_name="تایید ایمیل")
    date_of_birth = models.DateField(verbose_name="تاریخ تولد", null=True, blank=True)
    is_panel_admin = models.BooleanField(default=False, verbose_name='دسترسی به پنل ادمین')
    dashboards = models.ManyToManyField(Dashboard, verbose_name="دسترسی داشبوردها", blank=True)
    
    USERNAME_FIELD = 'phone'
    objects = UserManager()

    class Meta:
        verbose_name_plural = 'کاربران'
        verbose_name = 'کاربر'

    def get_date_joined(self):
        if self.date_joined:
            return datetime2jalali(self.date_joined).strftime("%H:%M - %Y/%m/%d")
        return 'بدون تاریخ'
    get_date_joined.short_description = 'تاریخ و زمان عضویت'

    def get_date_joined__date(self):
        if self.date_joined:
            return datetime2jalali(self.date_joined).strftime("%Y/%m/%d")
        return 'بدون تاریخ'  
    get_date_joined__date.short_description = 'تاریخ عضویت'

    def get_last_update(self):
        if self.last_update:
            return datetime2jalali(self.last_update).strftime("%H:%M - %Y/%m/%d")
        return 'بدون تاریخ'
    get_last_update.short_description = 'آخرین بروزرسانی'

    def get_last_login(self):
        if self.last_login:
            return datetime2jalali(self.last_login).strftime("%H:%M - %Y/%m/%d")
        return "تاکنون وارد سایت نشده است."
    get_last_login.short_description = 'آخرین ورود'

    def get_date_of_birth(self):
        if self.date_of_birth:
            return date2jalali(self.date_of_birth).strftime("%Y/%m/%d")
        return ''
    get_date_of_birth.short_description = 'تاریخ تولد'

    def __str__(self):
        if self.get_full_name():
            return self.get_full_name()
        return self.username

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.__previous_phone = self.phone
            self.__previous_email = self.email

    def save(self, *args, **kwargs):   
        if self.__previous_phone != self.phone:
            self.valid_phone = False
        if self.__previous_email != self.email:
            self.valid_email = False
        super(User, self).save()

    def get_full_name(self):
        if self.first_name or self.last_name:
            return f'{self.first_name} {self.last_name}'
        return None 
    

class VerificationCode(General):
    SUBJECT_CHOICES = [
        ("phone", "تلفن همراه"),
        ("email", "ایمیل"),
    ]
    STATUS_CHOICES =[
        (0, "نامعتبر"),
        (1, "معتبر"),
        (2, "اعمال شده"),
    ]
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, verbose_name="نوع کد تایید")
    code = models.CharField(max_length=10, blank=True, editable=False, unique=True,
           default=generate_new_verification_code, verbose_name="کد تایید")
    status = models.PositiveSmallIntegerField(default=1, choices=STATUS_CHOICES, verbose_name="وضعیت کد")
    attempts =  models.PositiveSmallIntegerField(default=0, verbose_name="تعداد تلاش")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر", null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ایجاد")


    class Meta:
        verbose_name = 'کد تایید'
        verbose_name_plural = 'کدهای تایید'

    def __str__(self):
        return f"{self.subject} - {self.code}"
    
    @property
    def get_status(self):
        return dict(self.STATUS_CHOICES)[self.status]

    @property
    def get_subject(self):
        return dict(self.SUBJECT_CHOICES)[self.subject]


class Wallet(General):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.BigIntegerField(default=0)
    
    class Meta:
        verbose_name = 'کیف پول'
        verbose_name_plural = 'کیف های پول'

        
    def __str__(self):
        return f'{self.user}: {self.balance}'

    def get_formatted_balance(self):
        return '{:,.0f}'.format(self.balance)


class TransactionHistory(General):
    CHOICE_1 = 'C1'
    CHOICE_2 = 'C2'

    MY_CHOICES = [
        (CHOICE_1, 'واریز'),
        (CHOICE_2, 'برداشت'),
    ]

    ADMIN = 'A'
    USER = 'U'

    CHARGE_BY = [
        (ADMIN, 'ادمین'),
        (USER, 'کاربر'),
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.BigIntegerField()
    transaction_type = models.CharField(max_length=10, choices=MY_CHOICES, default=CHOICE_1)
    charge_by = models.CharField(max_length=10, choices=CHARGE_BY, blank=True, null=True)
    message = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return f'{self.wallet.user} {self.amount} {self.transaction_type}'

    def get_created_at_jalali(self):
        if self.created_at is not None:
            return date2jalali(self.created_at).strftime('%Y/%m/%d')
        else:
            return ''


