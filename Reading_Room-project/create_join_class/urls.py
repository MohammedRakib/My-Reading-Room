from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('signup/', views.signup_user, name='signup_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('accounts/profile/', views.home_classroom, name='home_classroom'),
    path('accounts/profile/uploadimage', views.uploadFaceImage, name='uploadFaceImage'),

    path('create/class/', views.create_class, name='create_class'),
    path('join/class/', views.join_class, name='join_class'),
    path('view/createdclass/<int:classroom_pk>', views.viewcreatedclassroom, name='viewcreatedclassroom'),
    path('view/joinedclass/<int:classroom_pk>', views.viewjoinedclassroom, name='viewjoinedclassroom'),
    path('view/createdclass/<int:created_pk>/viewCreatedReadingMaterial', views.viewCreatedReadingMaterial,
         name='viewCreatedReadingMaterial'),
    path('view/joinedclass/<int:joined_pk>/viewJoinedReadingMaterial', views.viewJoinedReadingMaterial,
         name='viewJoinedReadingMaterial'),
    path('viewpdf/<path:filename>/<int:material_id>', views.viewPDF,
         name='viewPDF'),
    path('view/createdclass/<int:classroom_pk>/uploadReadingMaterial/', views.uploadReadingMaterial,
         name='uploadReadingMaterial'),
    path('view/createdclass/<int:classroom_pk>/deleteReadingMaterial/<int:readingMaterial_pk>',
         views.deleteReadingMaterial, name='deleteReadingMaterial'),
    # unit test till above urls

    # development purpose
    # path('push/<int:readingMaterial_id>/push/info/', views.push_reading_info, name='view_reading_info'),

    path('view_reading_info/<int:readingMaterial_id>/', views.view_reading_info, name='view_reading_info'),
    path('push_reading_info/<int:readingMaterial_id>/', views.push_reading_info, name='push_reading_info'),

    path('facedetect/', views.facedetect, name='facedetect'),


]
