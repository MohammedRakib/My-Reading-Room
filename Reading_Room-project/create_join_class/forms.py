from django.forms import ModelForm
from .models import ClassRoom


class CreateClassRoomForm(ModelForm):
    class Meta:
        model = ClassRoom
        fields = ['name', 'section']
