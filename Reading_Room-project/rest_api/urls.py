from django.urls import path
from . import views


urlpatterns = [
    # auth
    path('login/', views.login),
    path('signup/', views.signup),

    #class
    path('home_classroom_create/', views.HomeClassroomCreateClass.as_view(), name='HomeClassroomCreateClass'),
    path('home_classroom_view_joined/', views.HomeClassroomJoinedClass.as_view(), name='HomeClassroomJoinedClass'),
    path('get_classroom_id/', views.getAclassroomID, name='getAclassroomID'),
    path('classroom/<int:pk>/join/', views.MakeClassRoomJoinClass.as_view(), name='MakeClassRoomJoinClass'),
    path('classroom/<int:classroom_id>/view_materials/', views.ViewFileAPIView.as_view(), name='ViewFileAPIView'),
    path('reading_info/<int:readingMaterial_id>/view/', views.ReadingInfoAPIView.as_view(), name='ReadingInfoAPIView'),
]