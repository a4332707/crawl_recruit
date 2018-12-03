from django.urls import path

from search_app import views

urlpatterns = [
    # path('search/',views.search,name='search'),
    path('page/',views.page,name='page'),
    path('main/',views.main,name='main'),
    path('vague/',views.search_vague,name='vague'),
    path('colume/', views.column, name='column'),
    path('pie/', views.pie, name='pie'),
    path('map/', views.map, name='map'),
    path('line/', views.line, name='line'),
    path('introduce/', views.introduce, name='introduce'),

]