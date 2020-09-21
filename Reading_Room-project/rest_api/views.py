from rest_framework import generics, permissions
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from .serializers import *
import uuid
from django.db import IntegrityError


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


@csrf_exempt
def signup(request):
    if request.method == "POST":
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(data['username'], password=data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=201)
        except IntegrityError:
            # status 400 means bad request
            return JsonResponse({'error': 'Username is already take!'}, status=400)


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


class MakeClassRoomJoinClass(generics.UpdateAPIView):
    serializer_class = JoinAClassSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ClassRoom.objects.exclude(students__in=[self.request.user.id])

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.instance.students.add(self.request.user)
        serializer.save()


@csrf_exempt
def getAclassroomID(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        try:
            classObj = ClassRoom.objects.get(classCode=data['classCode'])
            return JsonResponse({'token': str(classObj.id)}, status=200)
            # if classObj.teacher==request.user:
            #     return JsonResponse({'token': 'You are the teacher of this class'}, status=200)
            # else:
        except ClassRoom.DoesNotExist:
            return JsonResponse({'token': 'No class found with that class code'}, status=201)
