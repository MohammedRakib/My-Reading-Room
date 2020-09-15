from rest_framework import serializers
from create_join_class.models import *


class ClassRoomSerializer(serializers.ModelSerializer):
    classCode = serializers.ReadOnlyField()
    # students = serializers.ReadOnlyField()

    class Meta:
        model = ClassRoom
        fields = ['id', 'name', 'section', 'classCode', 'students']


class ClassRoomJoinSerializer(serializers.ModelSerializer):
    # classCode = serializers.ReadOnlyField()
    # students = serializers.ReadOnlyField()

    class Meta:
        model = ClassRoom
        fields = ['id', 'name', 'section', 'classCode', 'teacher', 'students']