from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('signup/', views.signup_user, name='signup_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('accounts/profile/', views.home_classroom, name='home_classroom'),

    path('create/class/', views.create_class, name='create_class'),
    path('join/class/', views.join_class, name='join_class'),



]