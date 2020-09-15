from django.forms import ModelForm
from django import forms
from .validators import validate_file_extension, validate_image_extension
from .models import *


class CreateClassRoomForm(ModelForm):
    class Meta:
        model = ClassRoom
        fields = ['name', 'section']


class ReadingMaterialForm(ModelForm):

    # def __init__(self, user, *args, **kwargs):
    #     super(ReadingMaterialForm, self).__init__(*args, **kwargs)
    #     self.fields['classroom'].queryset = ClassRoom.objects.filter(teacher=user)
    class Meta:
        model = ReadingMaterial
        fields = ['name', 'readingFile']


class FaceImageForm(forms.Form):
    imageFile = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),
                                validators=[validate_image_extension])

    class Meta:
        model = FaceImage
        fields = ['imageFile']
