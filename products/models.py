from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.utils import timezone
from jalali_date import datetime2jalali, date2jalali
from .managers import PublishedManager
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator


User = get_user_model()

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر')
    first_name = models.CharField(max_length=300, verbose_name='نام')
    last_name = models.CharField(max_length=300, verbose_name='نام خانوادگی')
    slug = models.SlugField(blank=True, null=True, unique=True, \
                            allow_unicode=True, verbose_name='پیوند یکتا')
    phone = models.CharField(verbose_name="تلفن همراه", null=True, blank=True, max_length=11, unique=True)
    image = models.ImageField(verbose_name='عکس', upload_to='professor_images/')
    specialty = models.CharField(max_length=500, blank=True, null=True, verbose_name='تخصص ها')
    created_at = models.DateTimeField(verbose_name='تاریخ ایجاد', default=timezone.now)
    updated_at = models.DateTimeField(verbose_name='اخرین تغییر', auto_now=True)
    is_active = models.BooleanField(verbose_name='وضعیت', default=True)
    student_count = models.PositiveIntegerField(default=0, verbose_name="دانشجوها")

    class Meta:
        verbose_name = 'استاد'
        verbose_name_plural = 'اساتید'
    
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            value = self.full_name
            self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def increment_student_count(self):
        self.student_count += 1
        self.save()

    @property
    def get_student_count(self):
        return self.student_count
    
    def get_created_at_jalali(self):
        if self.created_at is not None:  
            return date2jalali(self.created_at).strftime('%Y/%m/%d')
        else:
            return ''
    
    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name
    
    def get_is_active(self):
        return 'بله' if self.is_active else 'خیر'
    
class BaseModel(models.Model):
    title = models.CharField(max_length=500, verbose_name='نام')
    slug = models.SlugField(blank=True, null=True, unique=True, \
                            allow_unicode=True, verbose_name='پیوند یکتا')
    description = RichTextField(verbose_name='توضیحات')
    meta_title = models.CharField(max_length=500, verbose_name='نام کوتاه')
    meta_description = models.TextField(verbose_name='توضیحات کوتاه', max_length=500)
    created_at = models.DateTimeField(verbose_name='تاریخ ایجاد', default=timezone.now)
    updated_at = models.DateTimeField(verbose_name='اخرین تغییر', auto_now=True)
    is_active = models.BooleanField(verbose_name='وضعیت', default=True)
    student_count = models.PositiveIntegerField(default=0, verbose_name="تعداد دانشجو")
    index = models.PositiveBigIntegerField(verbose_name='ترتیب نمایش', null=True, blank=True)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        abstract = True
        ordering = ('-index', )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            value = self.title
            self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def increment_student_count(self):
        self.student_count += 1
        self.save()

    @property
    def get_student_count(self):
        return self.student_count
    
    def get_created_at_jalali(self):
        if self.created_at is not None:  
            return date2jalali(self.created_at).strftime('%Y/%m/%d')
        else:
            return ''
    
    def get_is_active(self):
        return 'بله' if self.is_active else 'خیر'

class Category(BaseModel):
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, \
                                        related_name='subcategories', verbose_name='دسته والد')
    picture = models.ImageField(verbose_name='عکس گروه محصول', upload_to='category_images/')
    
    class Meta:
        verbose_name_plural = 'دسته محصول'
        verbose_name = 'دسته محصول'
        ordering = ('index', )

    def get_packages_count(self):
        return self.packages.count()
    
class Package(BaseModel):
    pre_video = models.TextField(verbose_name='لینک ویدیوی پیش نمایش')
    image = models.ImageField(verbose_name='عکس', upload_to='package_images/')
    price = models.PositiveIntegerField(verbose_name='قیمت')
    price_with_discount = models.PositiveIntegerField(verbose_name='قیمت با تخفیف', blank=True, null=True)
    day_limit = models.PositiveBigIntegerField(verbose_name='تعداد روز های قابل استفاده')
    categories = models.ManyToManyField(Category, blank=True, verbose_name='دسته‌ها', related_name='packages')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'لیست دسته بندی'
        ordering = ('index', )

    def get_absolute_url(self):
        return reverse("edu:package_detail", kwargs={'package_slug': self.slug})

    def get_total_price_of_courses(self):
        total_price = 0
        for course in self.courses.all():
            total_price += course.price
        return total_price
    
    def get_total_price_with_discount_of_courses(self):
        total_price = 0
        for course in self.courses.all():
            total_price += course.price_with_discount
        return total_price
    
    def get_your_profit(self):
        if self.price_with_discount:
            return self.get_total_price_of_courses() - self.price_with_discount
        else:
            return self.get_total_price_of_courses() - self.price

    def get_courses_count(self):
        return self.courses.count()
    
    def get_all_categories(self):
            return ', '.join(self.categories.all().values_list('title', flat=True))
    
    @staticmethod
    def format_price_with_commas(price):
        return '{:,.0f}'.format(price)

    def formatted_price(self):
        return self.format_price_with_commas(self.price)
    
    def formatted_paid_price(self):
        return self.format_price_with_commas(self.price_with_discount) if self.price_with_discount else self.format_price_with_commas(self.price)
    
    def formatted_price_with_discount(self):
        return self.format_price_with_commas(self.price_with_discount)
    
    def formmated_total_price_of_courses(self):
        return self.format_price_with_commas(self.get_total_price_of_courses())

    def formmated_total_price_with_discount_of_courses(self):
        return self.format_price_with_commas(self.get_total_price_after_discount_of_courses())
    
    def formmated_your_profit(self):
        return self.format_price_with_commas(self.get_your_profit())
    
    def display_profit(self):
        if self.get_your_profit() < 0:
            return "-"
        else:
            return self.formmated_your_profit()
    
class Course(BaseModel):
    pre_video = models.TextField(verbose_name='لینک ویدیوی پیش نمایش')
    professor = models.ForeignKey(Professor, related_name='courses', on_delete=models.SET_NULL,
                                   blank=True, null=True, verbose_name='استاد مجموعه')
    image = models.ImageField(verbose_name='عکس', upload_to='course_images/')
    price = models.PositiveIntegerField(verbose_name='قیمت')
    price_with_discount = models.PositiveIntegerField(verbose_name='قیمت با تخفیف', blank=True, null=True)
    day_limit = models.PositiveBigIntegerField(verbose_name='تعداد روز های قابل استفاده')
    categories = models.ManyToManyField(Category, blank=True, verbose_name='دسته‌ها', related_name='courses')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, blank=True, null=True, 
                                verbose_name='دسته بندی مربوطه', related_name='courses')

    class Meta:
        verbose_name = 'مجموعه'
        verbose_name_plural = 'لیست مجموعه'
        ordering = ('index', )

    def get_absolute_url(self):
        return reverse("edu:course_detail", kwargs={'course_slug': self.slug})
    
    def get_chapters_count(self):
        return self.chapters.count()
    
    def is_course(self):
        return True
    
    def get_price(self):
        if self.price and self.price !=0:
            return str(self.price) + ' تومان'
        else:
            return 'رایگان'      

    @staticmethod
    def format_price_with_commas(price):
        return '{:,.0f}'.format(price)

    def formatted_price(self):
        return self.format_price_with_commas(self.price)     

    def formatted_price_with_discount(self):
        return self.format_price_with_commas(self.price_with_discount)     

    def formatted_paid_price(self):
        return self.format_price_with_commas(self.price_with_discount) if self.price_with_discount else self.format_price_with_commas(self.price)
    
class Chapter(BaseModel):
    image = models.ImageField(verbose_name='عکس', upload_to='chapter_images/')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='مجموعه مربوطه', related_name='chapters')
    
    class Meta:
        verbose_name = 'فصل'
        verbose_name_plural = 'لیست فصل ها'
        ordering = ('index', )

    def get_parts_count(self):
        return self.parts.count()
    
    def get_absolute_url(self):
        return reverse("edu:chapter_slug", kwargs={'chapter_slug': self.slug})
      
class Part(BaseModel):
    part_index = models.IntegerField(verbose_name='شماره محصول')
    part_time = models.CharField(max_length=100, verbose_name='زمان ویدئو')
    price = models.PositiveIntegerField(verbose_name='قیمت')
    price_with_discount = models.PositiveIntegerField(verbose_name='قیمت با تخفیف', blank=True, null=True)
    image = models.ImageField(verbose_name='عکس', upload_to='part_images/')
    image_2 = models.ImageField(verbose_name='عکس دوم(سایز مستطیلی)', upload_to='part/images/', blank=True, null=True)
    video_link = models.TextField(verbose_name='لینک ویدیو')
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='فصل مربوطه', related_name='parts')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='مجموعه مربوطه', related_name='parts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, verbose_name='دسته بندی مربوطه', related_name='parts')
    
    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'لیست محصول'
        ordering = ('index', )
    
    def get_absolute_url(self):
        return reverse("edu:part_detail", kwargs={'part_slug': self.slug})

    @staticmethod
    def format_price_with_commas(price):
        return '{:,.0f}'.format(price)
        
    def formatted_price(self):
        return self.format_price_with_commas(self.price)
    
    def formatted_discount_price(self):
        if self.price_with_discount:
            return self.format_price_with_commas(self.price_with_discount)
        return None
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments', verbose_name='کاربر')
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, blank=True, null=True, related_name='course_comments', verbose_name='مجموعه')
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True, blank=True,\
                                 related_name='package_comments', verbose_name='دسته بندی')
    rate = models.IntegerField(verbose_name='امتیاز', validators=[MinValueValidator(1), MaxValueValidator(5)])
    content = models.TextField(verbose_name='متن نظر')
    created_at = models.DateTimeField(verbose_name='تاریخ ایجاد', default=timezone.now)
    updated_at = models.DateTimeField(verbose_name='اخرین تغییر', auto_now=True)    
    is_active = models.BooleanField(verbose_name='وضعیت', default=False)
    index = models.PositiveBigIntegerField(verbose_name='ترتیب نمایش', null=True, blank=True)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'لیست نظرات'
        ordering = ('index', )
        

    def __str__(self):
        return f'{self.user} - {self.value}'
        
    def get_created_at_jalali(self):
        if self.created_at is not None:  
            return date2jalali(self.created_at).strftime('%Y/%m/%d')
        else:
            return ''

    def __str__(self):
        if self.package:
            return f"{self.user} => {self.rate} for {self.package}"
        else:
            return f"{self.user} => {self.rate} for {self.user}"
        
            
    def get_created_at_jalali(self):
        if self.created_at is not None:  
            return date2jalali(self.created_at).strftime('%Y/%m/%d')
        else:
            return ''

    def get_is_active(self):
        return 'فعال' if self.is_active else 'غیرفعال'
