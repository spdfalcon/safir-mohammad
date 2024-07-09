# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - sharifdata sdata.ir
"""

from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import User
from django.db.models import Q


# ------------------------------ User Login ------------------------------
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "نام کاربری",
                "class": "form-control",
                "title": ""
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "کلمه عبور",
                "class": "form-control",
                "title": ""
            }
        ))
    

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone']


    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'autofocus': 'autofocus'})
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

        for visible in self.visible_fields():
            visible.field.widget.attrs['title'] = ''

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        
        # Create a username based on the phone number
        phone_number = self.cleaned_data.get('phone', '')
        user.username = phone_number

        if commit:
            user.save()

        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']

