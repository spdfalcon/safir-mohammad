from django import forms
from .models import Message, DefaultMessage
from main.models import MainBanner



class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('body', )
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': 'پیامتان را بنویسید ...'})
        }
        

class DefaultMessageForm(forms.ModelForm):
    class Meta:
        model = DefaultMessage
        fields = ('body', )
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': 'پیامتان را بنویسید ...'})
        }


class MainBannerForm(forms.ModelForm):
    class Meta:
        model = MainBanner
        fields = ('title', 'image')
        
         