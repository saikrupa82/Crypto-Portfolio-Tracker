from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_management.settings')
app=Celery('user_management')
app.conf.enable_utc=False
app.conf.update(timezone='Asia/Kolkata')

app.config_from_object('django.conf:settings', namespace='CELERY')

#Celery Beat Settings
app.conf.beat_schedule = {
"Update_daily_stats_database":{
    'task': 'users.tasks.update_daily_stats',
    'schedule': crontab(hour=23, minute=59)}
    ,
    "check_reminder_and_send_mail" :{
    'task': 'users.tasks.check_reminder',
    'schedule': crontab(minute=0, hour='*/1')
    }

}





app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

