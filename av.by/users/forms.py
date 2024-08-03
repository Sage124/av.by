from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import *

# форма для создания нового пользака
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'photo')

# форма для отправки собщений
class SendMessageForm(forms.Form):
    message = forms.CharField(label='Текст сообщения', widget=forms.Textarea)
    # recipients = forms.ModelMultipleChoiceField(label='Кому', queryset=User.objects.all())
    # send_date = forms.DateField(label='Дата отправки', widget=forms.DateInput(attrs={'type': 'date'}))
