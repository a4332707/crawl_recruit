from django.contrib import admin
from django.urls import path, include

from lr_app import views

urlpatterns = [
    path('login/',views.login,name='login'),
    path('login/logic/',views.login_logic,name='login_logic'),

    path('register/',views.register,name='register'),
    path('register/logic/',views.register_logic,name='register_logic'),
    path('ajax_telephone/',views.ajax_telephone,name='ajax_telephone'),
    path('ajax_email/',views.ajax_email,name='ajax_email'),
    path('check_email/',views.check_email,name='check_email'),
    path('get_captcha/',views.get_captcha,name='get_captcha'),
    path('ajax_username_password/',views.ajax_username_password,name='ajax_username_password'),

]