from django.db.models import *
import requests
from core.settings import SABANOVIN_SMS_API_KEY, SABANOVIN_SMS_GATEWAY
from .models import SmsLog
from io import BytesIO
import xlsxwriter
from datetime import datetime
from jalali_date import datetime2jalali
from django.http import HttpResponse



def send_sms(data, subject, user=None):
    phone = data.get('phone')
    text = data.get('text')
    url =  f'https://api.sabanovin.com/v1/{SABANOVIN_SMS_API_KEY}/sms/send.json?gateway={SABANOVIN_SMS_GATEWAY}&to={phone}&text={text}'
    status = True
    try:
        r = requests.get(url)
    except Exception as e: 
        new_sms_log = SmsLog(is_sent=False)
        new_sms_log.subject = subject
        new_sms_log.description = str(e)
        if user:
            new_sms_log.user = user
        new_sms_log.status_code = 999
        new_sms_log.save()
        status = False
        return status
    else:
        if r.status_code == 200:
            new_sms_log = SmsLog(is_sent=True)
        else:
            status = False
            new_sms_log = SmsLog(is_sent=False)
        new_sms_log.status_code = r.status_code
        new_sms_log.subject = subject
        if user:
            new_sms_log.user = user
        
        new_sms_log.save()
        return status


def export_excel(queryset):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    
    model_name = queryset.model.__name__
    today = datetime2jalali(datetime.now()).strftime('%Y-%m-%d__%H-%M')


    if model_name == 'Order':
        table_name = 'orders'
        field_verbose_names = ["نام", "نام خانوادگی", "شماره تلفن", "ایمیل", "تاریخ ایجاد", "پرداخت شده؟", 
                               "تاریخ پرداخت", "قیمت", "قیمت بعد از تخفیف", "شماره پیگیری پرداخت", "ایتم ها"]
        data = []
        
        for order in queryset:
            row = [
                order.user.first_name,
                order.user.last_name,
                order.user.phone,
                order.user.email,
                order.get_created_at_jalali(),
                order.get_is_paid(),
                order.get_paid_at_jalali() or '_',
                order.formatted_price(),
                order.formatted_price_after_discount(),
                order.ref_id or '_',
                order.get_item_titles() or '_'
            ]
            data.append(row)

    elif model_name == 'User':
        table_name = 'users'
        field_verbose_names = ["نام کاربری", "نام", "نام خانوادگی", "تاریخ ثبت نام", "شماره تلفن", "ایمیل", "تاریخ تولد", 
                               "دسترسی به پنل ادمین؟", "فعال بودن", "ابرکاربر؟", "وضعیت کارمندی؟", 'دسترسی داشبورد ها']
        data = []
        for user in queryset:
            row = [
                user.username,
                user.first_name or '_', 
                user.last_name or '_', 
                user.get_date_joined(),
                user.phone, 
                user.email or '_', 
                user.get_date_of_birth() or '_', 
                'بله' if user.is_panel_admin else 'خیر', 
                'بله' if user.is_active else 'خیر', 
                'بله' if user.is_superuser else 'خیر', 
                'بله' if user.is_staff else 'خیر', 
                ', '.join([str(dashboard) for dashboard in user.dashboards.all()]) or '_'
            ]
            data.append(row)

    elif model_name == 'Professor':
        table_name = 'professors'
        field_verbose_names = ["نام", "نام خانوادگی", "شماره تلفن", "عکس پروفایل", "تخصص ها", "تاریخ ایجاد", "فعال بودن",
                                "تعداد دانشجوها"]
        
        data = []
        for professor in queryset:
            row = [ 
                professor.first_name, 
                professor.last_name,
                professor.phone, 
                professor.image.url, 
                professor.specialty, 
                professor.get_created_at_jalali(), 
                professor.get_is_active(), 
                professor.student_count,
            ]
            data.append(row)

    elif model_name == 'Category':
        table_name = 'categories'
        field_verbose_names = ["دسته بندی والد", "عنوان", "توضیحات", "عنوان متا", "توضیحات متا", "عکس", "تاریخ ایجاد", 
                               "فعال بودن", "تعداد دانشجو"]
        data = []
        for category in queryset:
            row = [
                category.parent_category or '_', 
                category.title, 
                category.description, 
                category.meta_title, 
                category.meta_description, 
                category.picture.url, 
                category.get_created_at_jalali(), 
                category.get_is_active(), 
                category.student_count
            ]
            data.append(row)
    
    elif model_name == 'Package':
        table_name = 'packages'
        field_verbose_names = ["عنوان", "توضیحات", "عنوان متا", "توضیحات متا", "عکس", "تاریخ ایجاد", 
                               "فعال بودن", "تعداد دانشجو", "ویدئو پیش نمایش", "قیمت", "قیمت بعد از تخفیف",
                              "تعداد روز های قابل استفاده", "دسته بندی ها"]
        data = []
        for package in queryset:
            row = [
                package.title, 
                package.description, 
                package.meta_title, 
                package.meta_description, 
                package.image.url, 
                package.get_created_at_jalali(), 
                package.get_is_active(), 
                package.student_count, 
                package.pre_video, 
                package.price, 
                package.price_with_discount or '_', 
                package.day_limit, 
                ', '.join([str(category) for category in package.categories.all()])
            ]
            data.append(row)
    
    elif model_name == 'Course':
        table_name = 'courses'
        field_verbose_names = ["عنوان", "توضیحات", "عنوان متا", "توضیحات متا", "عکس", "تاریخ ایجاد", 
                               "فعال بودن", "تعداد دانشجو", "ویدئو پیش نمایش", "استاد", "قیمت", "قیمت بعد از تخفیف",
                              "تعداد روز های قابل استفاده", "دسته بندی ها", "پکیج مربوطه"]
        
        data = []
        for course in queryset:
            row = [
                course.title, 
                course.description, 
                course.meta_title, 
                course.meta_description, 
                course.image.url, 
                course.get_created_at_jalali(), 
                course.get_is_active(), 
                course.student_count, 
                course.pre_video, 
                course.professor or '_',
                course.price, 
                course.price_with_discount or '_', 
                course.day_limit, 
                ', '.join([str(category) for category in course.categories.all()]), 
                course.package
            ]
            data.append(row)
    
    elif model_name == 'Chapter':
        table_name = 'chapters'
        field_verbose_names = ["عنوان", "توضیحات", "عنوان متا", "توضیحات متا", "عکس", "تاریخ ایجاد", 
                               "فعال بودن", "تعداد دانشجو", "دوره مربوطه"]
        
        data = []
        for chapter in queryset:
            row = [
                chapter.title, 
                chapter.description, 
                chapter.meta_title, 
                chapter.meta_description, 
                chapter.image.url, 
                chapter.get_created_at_jalali(), 
                chapter.get_is_active(), 
                chapter.student_count, 
                chapter.course or '_'
            ]
            data.append(row)
    
    elif model_name == 'Part':
        table_name = 'parts'
        field_verbose_names = ["عنوان", "توضیحات", "عنوان متا", "توضیحات متا", "عکس", "تاریخ ایجاد", 
                               "فعال بودن", "شماره قسمت", "زمان ویدئو", "قیمت", "قیمت با تخفیف", "ویدئو پیش نمایش",
                               "تعداد دانشجو", "دوره مربوطه", "فصل مربوطه", "دسته بندی مربوطه"] 
        
        data = []
        for part in queryset:
            row = [
                part.title, 
                part.description, 
                part.meta_title, 
                part.meta_description, 
                part.image.url, 
                part.get_created_at_jalali(), 
                part.get_is_active(), 
                part.part_index,
                part.part_time,
                part.price,
                part.price_with_discount or '_',
                part.student_count or '_', 
                part.course or '_', 
                part.chapter or '_', 
                part.category or '_'
            ]
            data.append(row)

    else:
        data = queryset.values()
        field_verbose_names = [field.verbose_name for field in queryset.model._meta.fields]

    title_cell_format = workbook.add_format({'bold': True})
    row_num = 0
    for col_num in range(len(field_verbose_names)):
        worksheet.write(row_num, col_num, field_verbose_names[col_num], title_cell_format)

    for row in data:
        row_num += 1
        for col_num in range(len(row)):
            worksheet.write(row_num, col_num, str(row[col_num]))

    workbook.close()

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment;filename="{table_name}__{today}.xlsx"'
    response.write(output.getvalue())

    return response