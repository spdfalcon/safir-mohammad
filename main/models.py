from django.db import models
from jalali_date import datetime2jalali, date2jalali
from django.core.validators import MaxLengthValidator


# ----------------------- General Models  -----------------------
class General(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')

    class Meta:
        abstract = True

    def get_created_at(self):
        return datetime2jalali(self.created_at).strftime('%H:%M - %Y/%m/%d')
    get_created_at.short_description = 'تاریخ ایجاد'

    def get_updated_at(self):
        return datetime2jalali(self.updated_at).strftime('%H:%M - %Y/%m/%d')
    get_updated_at.short_description = 'آخرین بروزرسانی'
# ----------------------- end General Models  -----------------------
    
class SmsLog(General):
    SUBJECT_CHOICES = [
        ('phone_verify', 'تایید موبایل'),
        ('course_expiration', 'یادآور زمان باقیمانده از مجموعه'),
        ('unreed_comments', 'کامنت‌های نخوانده'),
        ('other', 'سایر'),
        ('visa-request', 'درخواست ویزا'),
        ('visa-request-created-admin', 'ارسال اطلاعیه درخواست ویزا به ادمین')
    ]

    user = models.ForeignKey('accounts.User', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='کاربر')
    subject = models.CharField(max_length=30, choices=SUBJECT_CHOICES, default='other', verbose_name='موضوع')
    is_sent = models.BooleanField(default=True, verbose_name='وضعیت ارسال')
    status_code = models.PositiveSmallIntegerField(null=True, verbose_name='کد وضعیت')
    description = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = 'تاریخچه اس ام اس'
        verbose_name_plural = 'تاریخچه اس ام اس ها'
        ordering = ('-created_at', )


    
    def status_code_str(self):
        return self.status_code
    status_code_str.short_description = 'پیام وضعیت ارسال'

class Dashboard(models.Model):
    title = models.CharField(verbose_name="نام داشبورد", max_length=120)
    path = models.CharField(verbose_name="آدرس داشبورد", max_length=120, help_text="/panel/")

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'داشبورد'
        verbose_name_plural = 'داشبوردها'

class LoginPage(models.Model):
    image = models.ImageField(upload_to='login_page/', verbose_name='لوگو')
    background_image = models.ImageField(upload_to='login_page/', verbose_name='عکس پس زمینه')
    title = models.CharField(max_length=200, verbose_name='عنوان زیر لوگو', default='ورود به حساب کاربری')
    description = models.TextField(verbose_name='متن توضیحات', \
                                   default=' برای استفاده از مجموعه های آموزشی زبان سفیر، لطفا شماره موبایل خود را وارد کنید، کد تایید به این شماره پیامک خواهد شد ')


    class Meta:
        verbose_name = 'بخش ورود'
        verbose_name_plural = 'بخش ورود'

    def __str__(self) -> str:
        return self.title

class MainBanner(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    image = models.ImageField(upload_to='main_banner/', verbose_name='عکس لوگو')


    class Meta:
        verbose_name = 'بنر'
        verbose_name_plural = 'بنرها'

    def __str__(self) -> str:
        return self.title

class WebSites(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    link = models.CharField(max_length=200, verbose_name='لینک')
    image = models.ImageField(upload_to='main_banner/', verbose_name='عکس لوگو')

    class Meta:
        verbose_name = 'وبسایت'
        verbose_name_plural = 'وبسایت ها'

    def __str__(self):
        return self.title
    