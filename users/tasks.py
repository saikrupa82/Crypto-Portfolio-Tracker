from celery import shared_task
from django.core.mail import send_mail
import smtplib, ssl
from pycoingecko import CoinGeckoAPI
from .models import *
from django.contrib.auth import get_user_model

# from mylib import config, thread
config = 'sohanmah23@gmail.com'
class Mailer:

    """
    This script initiaties the email alert function.
    """
    def __init__(self):
        
        self.EMAIL = "saikrupar82@gmail.com"
    
        self.PASS = "schdog@82"
        self.PORT = 465
        self.server = smtplib.SMTP_SSL('smtp.gmail.com', self.PORT)

    def send(self, mail):
        self.server = smtplib.SMTP_SSL('smtp.gmail.com', self.PORT)
        self.server.login(self.EMAIL, self.PASS)
        SUBJECT = 'ALERT!'
        TEXT = f'Social distancing violations exceeded!'
        message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)

        # sending the mail
        self.server.sendmail(self.EMAIL, mail, message)
        self.server.quit()

@shared_task(bind=True)
def check_reminder (self):
    Users = get_user_model().objects.all()
    for user_curr in Users:
        Hold_obj = Holdings.objects.filter(user=user_curr)
        Rem_obj = AddReminder.objects.filter(user=user_curr)

        temp={}
        for i in Hold_obj:
            temp[i.symbol_name]=i.quantity

        cg = CoinGeckoAPI()
        prices=cg.get_price(ids=list(temp.keys()), vs_currencies='inr')
        sum=0
        for i in temp:
            sum+=prices[i]['inr']*temp[i]
        for reminder in Rem_obj:
            msg=''
            Flag = 0 
            if reminder.Above_below=="Above" and sum>reminder.Price:
                Flag =1
                msg ='your portfolio is above '+str(reminder.Price)
            elif reminder.Above_below=="Below" and sum<reminder.Price:
                Flag =1
                msg = 'your portfolio is below '+str(reminder.Price)
            if Flag==1:
                send_mail(
                    'Reminder',
                    msg+'\n'+reminder.Notes,
                    'saikrupar82@gmail.com',
                    [user_curr.email],
                    fail_silently=False,
                    auth_password='schdog@82',
                )
                reminder.delete()
            
    return " Done check reminder"

@shared_task(bind=True)
def update_daily_stats (self):
    Users = get_user_model().objects.all()
    for user_curr in Users:
        Hold_obj = Holdings.objects.filter(user=user_curr)
        temp={}
        for i in Hold_obj:
            temp[i.symbol_name]=i.quantity

        cg = CoinGeckoAPI()
        prices=cg.get_price(ids=list(temp.keys()), vs_currencies='inr')
        sum=0
        for i in temp:
            sum+=prices[i]['inr']*temp[i]
        daily_user=DailyStats(user=user_curr,
                            portfolio_value=sum
        )
        daily_user.save()
    return "done update daily stats"
