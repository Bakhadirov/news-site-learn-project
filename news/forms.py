from django import forms
from .models import News
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


class ContactForm(forms.Form):
    subject = forms.CharField(label='Theme',widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Text', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    captcha = CaptchaField()

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, label='Please enter your username',widget=forms.TextInput(attrs={
        'class': 'form-control'}))
    password = forms.CharField(label='Please enter your password', widget=forms.PasswordInput(attrs={
        'class': 'form-control', "rows": 5}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=150, label='Please enter your username',
                               help_text='maximum length 150 characters',
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control'}))
    password1 = forms.CharField(label='Please enter your password', widget=forms.PasswordInput(attrs={
        'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={
        'class': 'form-control'}))
    email = forms.EmailField(label='e-mail', widget=forms.EmailInput(attrs={
        'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-control'}),
        #     # 'email': forms.EmailInput(attrs={'class': 'form-control'}),
        #     # 'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
        #     # 'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        #
        # }


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        # fields = '__all__' #выбраны все поля в модели
        fields = ['title', 'content', 'is_published', 'category']  # проход по полям, какие оставлять
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'categore': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):  # ищет что то в начале строки,в частности цирфу d = digit
            raise ValidationError('Название не должно начинаться с цифры')
        return title
