# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - sharifdata sdata.ir
"""
from . import views

from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

app_name = 'accounts'

urlpatterns = [
    #-----------------------------Logout url ---------------------------------------
    path("logout/", LogoutView.as_view(), name="logout"),

    #-----------------------------Login/signup toghether ---------------------------------------
    path('login/', SMSLoginSignupView.as_view(), name="login"),
    path('signup/sms/verification/', SMSSignUpVerificationView.as_view(), name="sms-signup-verification"),
    path('sms-login-verification/<str:phone>/', SMSLoginVerificationView.as_view(), name='sms-login-verification'),

    path('not_access/', not_access, name='not_access')
]