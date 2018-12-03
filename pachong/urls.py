from django.urls import path

from pachong import views


urlpatterns = [
    path("login/",views.login,name="login"),
    path("register/",views.register,name="register"),
    path("main/",views.main,name="main"),
    path("introduce/",views.introduce,name="introduce"),
    path("menu/",views.menu,name="menu"),

    path("register_logic",views.register_logic,name="register_logic"),
    path("login_logic",views.login_logic,name="login_logic"),

    path("get_bar",views.get_bar,name="get_bar"),
    path("get_pie",views.get_pie,name="get_pie"),
    path("get_map",views.get_map,name="get_map"),
    ]