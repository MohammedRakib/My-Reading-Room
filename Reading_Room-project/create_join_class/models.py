from django.db import models
from django.contrib.auth.models import User
from .validators import validate_file_extension, validate_image_extension
from private_storage.fields import PrivateFileField
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


class ClassRoom(models.Model):
    name = models.CharField(max_length=100)
    section = models.IntegerField()
    classCode = models.CharField(max_length=6, null=True, blank=True, unique=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_of_the_class')
    students = models.ManyToManyField(User, blank=True, related_name='student_of_the_class')

    def __str__(self):
        return self.name + '.' + str(self.section)+' ID:'+str(self.id)


class ReadingMaterial(models.Model):
    name = models.CharField(max_length=100)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='classroom')
    readingFile = PrivateFileField(upload_to='uploads/ReadingMaterial/', validators=[validate_file_extension])
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploader')

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.readingFile.delete()  # delete instance path
        super().delete(*args, **kwargs)  # Call the "real" delete() method.


class ReadingInfo(models.Model):
    material_id = models.ForeignKey(ReadingMaterial, on_delete=models.CASCADE)
    material_info = models.JSONField(null=True)

    def __str__(self):
        return str(self.material_id)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'uploads/faceimage/user_{0}/{1}'.format(instance.name.id, filename)


class FaceImage(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student')
    imageFile = PrivateFileField(upload_to=user_directory_path, validators=[validate_image_extension])

    def __str__(self):
        return self.name.username + "." + str(self.imageFile.name)


# Receive the pre_delete signal and delete the file associated with the model instance.
@receiver(pre_delete, sender=FaceImage)
def FaceImage_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    if instance.imageFile.storage.exists(instance.imageFile.name):
        instance.imageFile.delete(False)
