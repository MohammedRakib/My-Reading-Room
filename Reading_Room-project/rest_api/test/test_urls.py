from django.test import SimpleTestCase
from django.urls import reverse, resolve
from rest_api.views import *


""" This class is for unit test API urls """
class TestUrls(SimpleTestCase):
    def test_HomeClassroomCreateClass(self):
        self.assertEqual(resolve(reverse('HomeClassroomCreateClass')).func.view_class, HomeClassroomCreateClass)

    def test_HomeClassroomJoinedClass(self):
        self.assertEqual(resolve(reverse('HomeClassroomJoinedClass')).func.view_class, HomeClassroomJoinedClass)

    def test_MakeClassRoomJoinClass(self):
        self.assertEqual(resolve(reverse('MakeClassRoomJoinClass', args=[123456])).func.view_class,
                         MakeClassRoomJoinClass)

    def test_ViewFileAPIView(self):
        self.assertEqual(resolve(reverse('ViewFileAPIView', args=[123456])).func.view_class, ViewFileAPIView)

    def test_ReadingInfoAPIView(self):
        self.assertEqual(resolve(reverse('ReadingInfoAPIView', args=[123456])).func.view_class, ReadingInfoAPIView)
