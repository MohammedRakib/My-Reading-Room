from django.test import SimpleTestCase
from django.urls import reverse, resolve
from create_join_class.views import *


""" This class is for unit test of create_join_class app's urls """
class TestUrls(SimpleTestCase):
    def test_index(self):
        url = reverse('index')  # to get the url of the parameter name
        # print(resolve(url))  # to the the url view function
        self.assertEqual(resolve(url).func, index)  # to compare two views

    def test_signup_user(self):
        self.assertEqual(resolve(reverse('signup_user')).func, signup_user)

    def test_logout_user(self):
        self.assertEqual(resolve(reverse('logout_user')).func, logout_user)

    def test_home_classroom(self):
        self.assertEqual(resolve(reverse('home_classroom')).func, home_classroom)

    def test_create_class(self):
        self.assertEqual(resolve(reverse('create_class')).func, create_class)

    def test_join_class(self):
        self.assertEqual(resolve(reverse('join_class')).func, join_class)

    def test_viewcreatedclassroom(self):
        self.assertEqual(resolve(reverse('viewcreatedclassroom', args=[123456])).func, viewcreatedclassroom)

    def test_viewjoinedclassroom(self):
        self.assertEqual(resolve(reverse('viewjoinedclassroom', args=[123456])).func, viewjoinedclassroom)

    def test_viewCreatedReadingMaterial(self):
        self.assertEqual(resolve(reverse('viewCreatedReadingMaterial', args=[123456])).func, viewCreatedReadingMaterial)

    def test_viewJoinedReadingMaterial(self):
        self.assertEqual(resolve(reverse('viewJoinedReadingMaterial', args=[123456])).func, viewJoinedReadingMaterial)

    def test_uploadReadingMaterial(self):
        self.assertEqual(resolve(reverse('uploadReadingMaterial', args=[123456])).func, uploadReadingMaterial)

    def test_deleteReadingMaterial(self):
        self.assertEqual(resolve(reverse('deleteReadingMaterial', kwargs={'classroom_pk': '123456', 'readingMaterial_pk':'123456'})).func, deleteReadingMaterial)
