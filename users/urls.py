from django.urls import path
from .views import *

urlpatterns = [
    path('home', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('',index,name='index'),
    path('news',news,name='news')
]
