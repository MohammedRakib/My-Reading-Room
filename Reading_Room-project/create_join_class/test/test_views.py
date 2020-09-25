from django.test import TestCase, Client
from django.urls import reverse
from create_join_class.models import *
import json


class TestViews(TestCase):

    # this method is going to run before every test
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user("Haq123", "12345678")

        self.index_url = reverse('index')
        self.signup_user = reverse('signup_user')
        self.logout_user = reverse('logout_user')
        self.home_classroom = reverse('home_classroom')
        self.create_class = reverse('create_class')

    def test_index_GET(self):
        # client = Client()  # setup-code
        # response = client.get(reverse('index'))  # test code

        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)  # assertion
        self.assertTemplateUsed(response, 'create_join_class/index.html')

    def test_index_POST(self):
        self.client.login(username="Haq123", password="12345678")
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)

    def test_signup_user_GET(self):
        response = self.client.get(self.signup_user)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_join_class/signupuser.html')

    def test_logout_user_POST(self):
        response = self.client.post(self.logout_user)
        self.assertEqual(response.status_code, 302)

    def test_home_classroom(self):
        self.client.login(username="Haq123", password="12345678")
        self.assertEqual(ClassRoom.objects.filter(teacher=self.user).count(), 0)
        self.assertEqual(ClassRoom.objects.filter(students__in=[self.user.id]).count(), 0)

    # def test_create_class_GET(self):
    #     self.client.login(username="Haq123", password="12345678")
    #     response = self.client.get(self.create_class)
    #     # self.assertEqual(response.status_code, 302)
    #     self.assertTemplateUsed(response, 'create_class.html')

