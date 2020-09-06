from django.db import models
from django.contrib.auth.models import User


class ClassRoom(models.Model):
    name = models.CharField(max_length=100)
    section = models.IntegerField()
    classCode = models.CharField(max_length=6, null=True, blank=True, unique=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_of_the_class')
    # students = models.ManyToManyField(User, null=True, blank=True)
    students = models.ManyToManyField(User, null=True, blank=True, related_name='student_of_the_class')
    # students = models.ManyToManyField(User, blank=True, related_name='student_list')

    def __str__(self):
        return self.name + '.' + str(self.section)


class ReadingMaterial(models.Model):
    name = models.CharField(max_length=100)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='classroom')
    readingFile = models.FileField(upload_to='uploads/ReadingMaterial/')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploader')

    def __str__(self):
        return self.name


class ReadingInfo(models.Model):
    material_id = models.ForeignKey(ReadingMaterial, on_delete=models.CASCADE)
    material_info = models.JSONField(null=True)

    def __str__(self):
        return str(self.material_id)



