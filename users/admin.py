from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register(Holdings)
admin.site.register(AddReminder)
admin.site.register(Transaction)
admin.site.register(DailyStats)
