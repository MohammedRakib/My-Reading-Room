from rest_framework import serializers
from create_join_class.models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'username']


class CustomClassRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClassRoom
        fields = ['name']


class ClassRoomSerializer(serializers.ModelSerializer):
    classCode = serializers.ReadOnlyField()
    students = UserSerializer(read_only=True, many=True)  # manyTomany fields need to serialize individually

    class Meta:
        model = ClassRoom
        fields = ['id', 'name', 'section', 'classCode', 'students']


class ClassRoomJoinedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = ['id', 'name', 'section', 'classCode', 'teacher', 'students']


class JoinAClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = ['id']
        read_only_fields = ['name', 'section', 'classCode', 'teacher', 'students', ]


class ReadingMaterialSerializer(serializers.ModelSerializer):
    classroom = CustomClassRoomSerializer(read_only=True, many=False)
    uploader = UserSerializer(read_only=True, many=False)

    class Meta:
        model = ReadingMaterial
        fields = ['name', 'classroom', 'readingFile', 'uploader']


class ReadingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingInfo
        fields = ['material_id', 'material_info', ]