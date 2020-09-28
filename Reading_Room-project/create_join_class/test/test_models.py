from django.test import TestCase, Client
from create_join_class.models import *
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
import json


""" This class is for unit testing of our model classes in create_join_class app's """
class TestModels(TestCase):

    def setUp(self):
        # self.client = Client()
        # self.user = User.objects.create_user("Haq123", "12345678")

        self.teacher1 = User.objects.create_user('Nbm', 'abcdef12')
        self.student1 = User.objects.create_user('Rakib', '123abc')
        self.student2 = User.objects.create_user('Sana', 'abc123')

        self.json_data = {
            self.student1.username: 20,
            self.student2.username: 25,
        }

        self.classroom1 = ClassRoom.objects.create(
            name="CSE327",
            section=1,
            classCode="ABCDEF",
            teacher=self.teacher1,
        )

        self.readingmaterial1 = ReadingMaterial.objects.create(
            name="CSE327_Course Outline",
            classroom=self.classroom1,
            uploader=self.teacher1,
        )
        self.readinginfo1 = ReadingInfo.objects.create(
            material_id=self.readingmaterial1,
            material_info=json.dumps(self.json_data)
        )
        self.faceimage = FaceImage.objects.create(
            name=self.student2,
            # imageFile=SimpleUploadedFile(name='IMG1.jpg', content=open('unit_test_static_files', 'rb').read(),content_type='image/jpeg')
        )

    def test_ClassRoom_model(self):
        self.assertEqual(self.classroom1.name, "CSE327")
        self.assertEqual(ClassRoom.objects.all().count(), 1)

    def test_ReadingMaterial_model(self):
        self.assertEqual(self.readingmaterial1.uploader, self.teacher1)
        self.assertEqual(ReadingMaterial.objects.all().count(), 1)

    def test_ReadingInfo_model(self):
        self.assertEqual(json.loads(self.readinginfo1.material_info), self.json_data)
        self.assertEqual(ReadingInfo.objects.all().count(), 1)

    def test_FaceImage_model(self):
        self.assertEqual(FaceImage.objects.all().count(), 1)


