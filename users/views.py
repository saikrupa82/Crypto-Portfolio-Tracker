from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import *
from json import dumps
import schedule
import time
from .forms import *


def home(request):
    return render(request, 'users/home.html')


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def index(request):
    submitted = False
         

    if request.method == 'POST':
        Add_Reminder_values = AddReminderForm(request.POST)
        Add_Transaction_Values = AddTransactionForm(request.POST)
        profile = Profile.objects.filter(user=request.user)
        if Add_Reminder_values.is_valid():
            # print(Add_Reminder_values)
            # print(Add_Reminder_values['Buy_Sell'].value())
            AddReminder_obj = AddReminder(user=request.user,
                                Price= Add_Reminder_values['Price'].value(),
                                 buy_sell= Add_Reminder_values['Buy_Sell'].value(),
                                Notes = Add_Reminder_values['Note'].value() )
            # cd = Add_Reminder_values.cleaned_data()
            # Add_Reminder_values['Username']=request.user
            # Add_Reminder_values = list(Add_Reminder_values)
            AddReminder_obj.save()
            messages.success(request, 'Your Reminder is updated successfully')
            Add_Reminder_values = AddReminderForm(request.POST)
            return redirect(to='index')
        if Add_Transaction_Values.is_valid() and request.method == 'POST':
            if Add_Transaction_Values['Buy_Sell'].value() =='Buy':
                Hold_obj = Holdings.objects.filter(user=request.user,symbol_name=request.POST.get('search_coin')).exists()
                if Hold_obj:
                    Hold_obj_update = Holdings.objects.get(user=request.user,symbol_name=request.POST.get('search_coin'))
                    Hold_obj_update.quantity += float(request.POST.get('quantity'))
                    Hold_obj_update.amount_spent += float(request.POST.get('quantity'))*float(request.POST.get('price_name'))
                    Hold_obj_update.save()
                    messages.success(request, 'Your Transaction is updated successfully')
                    Add_Reminder_values = AddTransactionForm(request.POST)
                else:
                    print(request.POST.get('search_coin'))
                    Hold_obj_add = Holdings(
                                            user=request.user,
                                            symbol_name = request.POST.get('search_coin'),
                                            quantity = request.POST.get('quantity'),
                                            amount_spent = float(request.POST.get('quantity'))*float(request.POST.get('price_name'))
                    )
                    Hold_obj_add.save()
                AddTransaction_obj = Transaction(user=request.user,
                                    price= request.POST.get('price_name'),
                                    buy_sell= Add_Transaction_Values['Buy_Sell'].value(),
                                    quantity = Add_Transaction_Values['quantity'].value(),
                                    symbol = request.POST.get('symbol'),
                                    symbol_name = request.POST.get('search_coin'),
                                    date = request.POST.get('date'))
                AddTransaction_obj.save()
                messages.success(request, 'Your Transaction is updated successfully')
                Add_Reminder_values = AddTransactionForm(request.POST)
            else:
                Hold_obj = Holdings.objects.filter(user=request.user,symbol_name=request.POST.get('search_coin')).exists()
                if Hold_obj:
                    Hold_obj_update = Holdings.objects.get(user=request.user,symbol_name=request.POST.get('search_coin'))
                    if Hold_obj_update.quantity >= float(Add_Transaction_Values['quantity'].value()):
                        AddTransaction_obj = Transaction(user=request.user,
                                    price= request.POST.get('price_name'),
                                    buy_sell= Add_Transaction_Values['Buy_Sell'].value(),
                                    quantity = Add_Transaction_Values['quantity'].value(),
                                    symbol = request.POST.get('symbol'),
                                    symbol_name = request.POST.get('search_coin'),
                                    date = request.POST.get('date'))
                        AddTransaction_obj.save()
                        messages.success(request, 'Your Transaction is updated successfully')
                        Add_Reminder_values = AddTransactionForm(request.POST)
                        Hold_obj_update.quantity -= float(request.POST.get('quantity'))
                        Hold_obj_update.amount_spent -= float(request.POST.get('quantity'))*float(request.POST.get('price_name'))
                        Hold_obj_update.save()
                    else:
                        messages.warning(request, "You don't Have enough Funds!!")
            
            Hold_obj = Holdings.objects.filter(user=request.user)
            temp={}
            for i in Hold_obj:
                temp[i.symbol_name]=i.quantity
            print(temp)
            return redirect(to='index')
    else:
        profile = Profile.objects.filter(user=request.user)
        Add_Reminder_values = AddReminderForm()
        Add_Transaction_Values = AddTransactionForm(request.POST)
        Hold_obj = Holdings.objects.filter(user=request.user)
        temp={}
        for i in Hold_obj:
            temp[i.symbol_name]=i.quantity
        temp=dumps(temp)
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'users/index.html',{'profile': profile,'Add_Reminder':Add_Reminder_values,'Add_Transaction':Add_Transaction_Values,'temp':temp})


@login_required
def news(request):
    return render(request, 'users/news.html')