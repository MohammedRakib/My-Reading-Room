from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('signup/', views.signup_user, name='signup_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('accounts/profile/', views.home_classroom, name='home_classroom'),

]