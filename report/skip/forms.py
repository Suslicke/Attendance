from urllib import request
from .models import Truancy
from django.forms import CheckboxInput, DateField, ModelForm, TextInput, DateInput, Form, CharField
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _

from django.conf import settings
import datetime



class TruancyForm(ModelForm):
    class Meta:
        model = Truancy
        fields = ['date', 'all_people', 'absenteeism', 'num_pairs']
        
        widgets = {
            "date": DateInput(attrs={'type': 'date',
                                     'name': 'date',
                                     'class': 'date',
                                     'id':'style_input',
                                     'value': datetime.datetime.today().strftime('%Y-%m-%d')}),
            "all_people": TextInput(attrs={'placeholder': 'Всего людей',
                                           'type': 'number',
                                           'class': 'all_people',
                                           'id': 'style_input'}),
            "absenteeism": TextInput(attrs={'placeholder': '  Отсутствующие',
                                            'type': 'number',
                                            'class': 'truancy',
                                            'id':'style_input'}),
            "num_pairs": TextInput(attrs={'placeholder': 'Всего пар',
                                          'type': 'number',
                                          'class':'total_lesson',
                                          'id': 'style_input'}),
            
        }
    
        
        
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        
        fields = ['username', 'password1', 'password2', 'is_staff']
        
        widgets = {
            "username": TextInput(attrs={'placeholder': 'Логин',
                                           'class': 'login',
                                           'type': 'login',
                                           'aria-describedby': 'loginHelp'}),
            "password1": TextInput(attrs={'placeholder': 'Пароль',
                                          'class': 'password',
                                           'type': 'password',
                                           }),
            "password2": TextInput(attrs={'placeholder': 'Пароль',
                                           'type': 'password',
                                           'class': 'password'}),
            "is_staff": CheckboxInput(attrs={'class': 'password'}),
            
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'placeholder': _('Пароль')})
        self.fields['password2'].widget.attrs.update({'placeholder': _('Повторите пароль')})


class LogInForm(AuthenticationForm):
    class Meta:
        model = User
        
        fields = ['username', 'password']
        
        widgets = {
            "username": TextInput(attrs={'placeholder': 'Логин',
                                         'type': 'login',
                                         'aria-describedby': 'loginHelp',
                                         'class': 'form-control'}),
            "password": TextInput(attrs={'placeholder': 'Пароль',
                                         'type': 'password',
                                         'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': _('Логин')})
        self.fields['username'].widget.attrs.update({'class': _('form-control')})
        self.fields['username'].widget.attrs.update({'id': _('exampleInputlogin')})
        self.fields['password'].widget.attrs.update({'class': _('form-control')})
        self.fields['password'].widget.attrs.update({'id': _('exampleInputPassword')})
        self.fields['password'].widget.attrs.update({'placeholder': _('Пароль')})


class DateForm(Form):
    
    start = DateField(widget=DateInput(attrs={'type': 'date',
                                              'class': 'date',
                                              'name':'date',
                                              'id':'style_input'}))
    end = DateField(widget=DateInput(attrs={'type': 'date',
                                            'name':'date',
                                            'class':'date',
                                            'id':'style_input'}))