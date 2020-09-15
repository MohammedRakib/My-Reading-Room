from django.urls import path
from . import views


urlpatterns = [
    # auth
    path('login/', views.login),

    #class
    path('home_classroom_create/', views.HomeClassroomCreateClass.as_view()),
    path('home_classroom_join/', views.HomeClassroomJoinClass.as_view()),
]