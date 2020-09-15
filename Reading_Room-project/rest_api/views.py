from rest_framework import generics, permissions
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from .serializers import *
import uuid
from rest_framework.exceptions import ValidationError


@csrf_exempt
def login(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is None:
            return JsonResponse({'token': 'Could not login, Please check username and password'}, status=201)
        else:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=200)


class HomeClassroomCreateClass(generics.ListCreateAPIView):
    serializer_class = ClassRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ClassRoom.objects.filter(teacher=self.request.user)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user, classCode=uuid.uuid4().hex[:6].upper())


class HomeClassroomJoinedClass(generics.ListAPIView):
    serializer_class = ClassRoomJoinedSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ClassRoom.objects.filter(students__in=[self.request.user.id])


# class MakeHomeClassroomJoinClass(generics.UpdateAPIView):
#     serializer_class = MakeClassRoomJoinSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self):
#         pass
#
#     def perform_create(self, serializer):
#         pass
#
#     def perform_update(self, serializer):
#         data = JSONParser().parse(self.request)
#         try:
#             classObj = ClassRoom.objects.get(classCode=data['classCode'])
#         except ClassRoom.DoesNotExist:
#             raise ValidationError('No class found with that class code')
#
#         if classObj.teacher == self.request.user:
#             raise ValidationError('You are the teacher of this class!')
#         else:
#             # classObj.students.add(self.request.user)
#             serializer.instance.students.add(self.request.user)
#             serializer.save()
