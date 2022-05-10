from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import *


class RegisterForm(UserCreationForm):
    # fields we want to include and customize in our form
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                               'class': 'form-control',
                                                               }))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                              'class': 'form-control',
                                                              }))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']


class AddReminderForm(forms.ModelForm):
    FILTER_CHOICES = (
        ('Buy', 'buy'),
        ('Sell', 'sell'),
    )
    Price = forms.IntegerField(required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Price',
                                                              'class': 'form-control',
                                                              }))
    Buy_Sell = forms.ChoiceField(required=True,choices = FILTER_CHOICES)
    Note = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = AddReminder
        fields = [ 'Price','Buy_Sell','Note']

class AddTransactionForm(forms.ModelForm):
    FILTER_CHOICES = (
        ('Buy', 'buy'),
        ('Sell', 'sell'),
    )
    symbol = forms.CharField(max_length=255,required=False,widget=forms.TextInput(attrs={'placeholder': 'select coin',
                                                              'class': 'form-control',
                                                              'id' : 'coin_symbol',
                                                              
                                                              })
                                )
    quantity= forms.IntegerField(required=False)
    # Price = forms.IntegerField(required=True,
    #                             widget=forms.TextInput(attrs={'placeholder': 'Price',
    #                                                           'class': 'form-control',
    #                                                           'id' : 'price',
    #                                                           }))
    Buy_Sell = forms.ChoiceField(choices = FILTER_CHOICES,required=False)

    class Meta:
        model = Transaction
        fields = ['symbol','quantity','Buy_Sell']