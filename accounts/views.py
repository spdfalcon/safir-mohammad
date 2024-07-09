# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - sharifdata sdata.ir
"""
# from products.models import Purchase
# Create your views here.
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.utils import timezone
from django.contrib import messages
from .models import VerificationCode, User
from main.utils import send_sms
from django.db.models import Q
from django.views import generic
from main.models import LoginPage


#-------------------------------Login/Signup -----------------------------
class SMSLoginSignupView(generic.View):
    template_name = 'accounts/sms_login_signup_form.html'

    def get(self, request, *args, **kwargs):
        login_page = LoginPage.objects.last()
        return render(request, self.template_name, {'login_page': login_page})

    def post(self, request, *args, **kwargs):
        context = {}
        phone = request.POST.get('phone', None)

        if phone:
            # Check if the user already exists
            user = User.objects.filter(Q(phone=phone))

            if user.exists():
                user = user.first()
                new_verify_code = VerificationCode.objects.create(user=user, subject="login")
                print(new_verify_code)
                text = f"""به اپلیکیشن سفیرمال خوش آمدید. رمز ورود یکبار مصرف
{new_verify_code.code}

safirmall.com

لغو11
                """
                
                data = {
                    "phone": phone,
                    "text": text,
                    "template": 'safir-login'
                }

                if send_sms(data, 'phone_verify', user):
                    # Save the phone number and verification code in the session for later use
                    request.session['login_phone'] = phone
                    request.session['login_verify_code'] = new_verify_code.code
                    # request.session['signup_verify_code_created'] = new_verify_code.created_at
                    
                    return redirect('accounts:sms-login-verification', phone=phone)
                else:
                    context['error'] = 'ارسال sms با خطا مواجه شد'
                    return render(request, self.template_name, context)
            else:
                # User doesn't exist, send signup SMS
                new_verify_code = VerificationCode.objects.create(subject="signup")
                
                text = f"""به اپلیکیشن سفیرمال خوش آمدید. رمز ورود یکبار مصرف
{new_verify_code.code}

safirmall.com

لغو11
                """
                
                data = {
                    "phone": phone,
                    "text": text,
                    "template": 'safir-login'
                }

                if send_sms(data, 'phone_verify'):
                    # Save the phone number and verification code in the session for later use
                    request.session['signup_phone'] = phone
                    request.session['signup_verify_code'] = new_verify_code.code
                    return redirect('accounts:sms-signup-verification')
                else:
                    context['error'] = 'خطا در ارسال کد ثبت نام'
                    return render(request, self.template_name, context)
        else:
            messages.error(request, 'شماره تلفن نامعتبر است')
            return render(request, self.template_name, {})

class SMSSignUpVerificationView(generic.View):
    template_name = 'accounts/sms_signup_confirm.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        phone = request.session.get('signup_phone')
        verify_code = request.POST.get('verify_code', None)
        context = {}

        if 'resend_code' in request.POST:
            print("resend code!!!")
            # Resend verification code
            new_verify_code = VerificationCode.objects.create(subject="login")
            request.session['signup_verify_code'] = new_verify_code.code
            
            text = f"""به اپلیکیشن سفیرمال خوش آمدید. رمز ورود یکبار مصرف
{new_verify_code.code}

safirmall.com

لغو11
            """
            
            data = {
                "phone": phone,
                "text": text,
                "template": 'safir-login'
            }

            if send_sms(data, 'phone_verify'):
                request.session['login_verify_code'] = new_verify_code.code
                messages.success(request, 'کد تایید جدید ارسال شد')
            else:
                context['error'] = 'ارسال sms با خطا مواجه شد'
        elif phone and verify_code:
            print("phone verify_code!!!!")
            if request.session.get('signup_verify_code') == verify_code:
                user = User.objects.create(phone=phone, username=phone, valid_phone=True)
                login(request, user)

                original_referrer = request.session.get('original_referrer', None)  
                if original_referrer:
                    return redirect(original_referrer)
                return redirect("main:home")
            else:
                context = {'error': 'کد نامعتبر است'}
        else:
            context['error'] = 'تلفن همراه نامعتبر است'

        return render(request, self.template_name, context)
    
class SMSLoginVerificationView(generic.View):
    template_name = 'accounts/sms_login_confirm.html'

    def get(self, request, *args, **kwargs):
        phone = kwargs.get('phone')
        return render(request, self.template_name, {'phone': phone})

    def post(self, request, *args, **kwargs):
        phone = kwargs.get('phone')
        verify_code = request.POST.get('verify_code', None)
        context = {}

        context['phone'] = phone

        if 'resend_code' in request.POST:
            # Resend verification code
            user = User.objects.filter(Q(phone=phone)).first()
            if user:
                new_verify_code = VerificationCode.objects.create(user=user, subject="login")
                
                text = f"""به اپلیکیشن سفیرمال خوش آمدید. رمز ورود یکبار مصرف
{new_verify_code.code}

safirmall.com

لغو11
                """
                
                data = {
                    "phone": phone,
                    "text": text,
                    "template": 'safir-login'
                }

                if send_sms(data, 'phone_verify', user):
                    request.session['login_verify_code'] = new_verify_code.code
                    messages.success(request, 'کد تایید جدید ارسال شد')
                else:
                    context['error'] = 'ارسال sms با خطا مواجه شد'
            else:
                context['error'] = 'کاربر یافت نشد!'
            return render(request, self.template_name, context)

        if phone and verify_code:
            try:
                the_user = User.objects.get(Q(phone=phone))
            except User.DoesNotExist:
                context['error'] = 'کاربر یافت نشد!'
                return render(request, self.template_name, context)

            verify = VerificationCode.objects.filter(user=the_user, subject='login', status=1).last()
            if verify:
                if verify.code == verify_code:
                    verify.attempts += 1
                    verify.status = 2
                    verify.save()
                    login(request, the_user)
                    original_referrer = request.session.get('next', None)  
                    if original_referrer:
                        return redirect(original_referrer)
                    return redirect("main:home")
                else:
                    verify.attempts += 1
                    if verify.attempts >= 5:
                        verify.status = 0
                    verify.save()
                    context['error'] = 'رمز ورود نامعتبر است!'
                    return render(request, self.template_name, context)
            else:
                context['error'] = 'رمز ورود منقضی شده است!'
                return render(request, self.template_name, context)
        else:
            context['error'] = 'تلفن همراه نامعتبر است'
            return render(request, self.template_name, context)

def not_access(request):
    return render(request, 'error_pages/page_403.html')




