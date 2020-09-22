import uuid
from django.http import FileResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CreateClassRoomForm, ReadingMaterialForm, FaceImageForm
from .models import *
from PIL import Image
import face_recognition
import json, os
import cv2
import numpy as np


def index(request):
    if request.method == 'GET':
        return render(request, 'create_join_class/index.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'create_join_class/index.html', {'form': AuthenticationForm(), 'error': 'Username '
                                                                                                           'or '
                                                                                                           'Password '
                                                                                                           'is '
                                                                                                           'incorrect'})
        else:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home_classroom')


def signup_user(request):
    if request.method == "GET":
        return render(request, 'create_join_class/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('home_classroom')
            except IntegrityError:
                return render(request, 'create_join_class/signupuser.html',
                              {'form': UserCreationForm(), 'error': 'Username is '
                                                                    'already taken!'})
        else:
            return render(request, 'create_join_class/signupuser.html',
                          {'form': UserCreationForm(), 'error': 'Password did not '
                                                                'match!'})


@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')


@login_required
def home_classroom(request):
    created_classes = ClassRoom.objects.filter(teacher=request.user)
    joined_classes = ClassRoom.objects.filter(students__in=[request.user.id])
    return render(request, 'create_join_class/home_classroom.html',
                  {'user': request.user, 'created_classes': created_classes, 'joined_classes': joined_classes})
    return render(request, 'create_join_class/home_classroom.html', {'user': request.user})


@login_required
def create_class(request):
    if request.method == "GET":
        return render(request, 'create_join_class/create_class.html', {'form': CreateClassRoomForm})
    else:
        try:
            form_data = CreateClassRoomForm(request.POST)
            new_class = form_data.save(commit=False)
            new_class.teacher = request.user
            new_class.classCode = uuid.uuid4().hex[:6].upper()
            new_class.save()
            return redirect('home_classroom')
        except ValueError:
            return render(request, 'create_join_class/create_class.html',
                          {'form': CreateClassRoomForm, 'error': 'Bad data passed in. Try again!'})


@login_required
def join_class(request):
    if request.method == "GET":
        return render(request, 'create_join_class/join_class.html')
    else:
        # checking if the class code that user entered does exist or not
        try:
            classobj = ClassRoom.objects.get(classCode=request.POST['classCode'])
        except ClassRoom.DoesNotExist:
            return render(request, 'create_join_class/join_class.html',
                          {'error': 'No class found with that class code!'})

        if classobj.teacher == request.user:
            return render(request, 'create_join_class/join_class.html', {'error': 'You are the teacher of this class!'})
        else:
            user = request.user
            classobj.students.add(user)
            return redirect('home_classroom')


@login_required
def viewcreatedclassroom(request, classroom_pk):
    classroom = get_object_or_404(ClassRoom, teacher=request.user, pk=classroom_pk)
    return render(request, "create_join_class/viewcreatedclassroom.html", {'classroom': classroom})


@login_required
def viewjoinedclassroom(request, classroom_pk):
    classroom = get_object_or_404(ClassRoom, students__in=[request.user.id], pk=classroom_pk)
    return render(request, "create_join_class/viewjoinedclassroom.html", {'classroom': classroom})


@login_required
def uploadReadingMaterial(request, classroom_pk):
    if request.method == 'GET':
        try:
            classroom = ClassRoom.objects.get(teacher=request.user, pk=classroom_pk)
        except ClassRoom.DoesNotExist:
            return render(request, "create_join_class/uploadReadingMaterial.html",
                          {'error': 'You don\'t have upload permissions to this classroom!'})
        form = ReadingMaterialForm()
        return render(request, "create_join_class/uploadReadingMaterial.html", {'form': form})
    else:
        form = ReadingMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            newmaterial = form.save(commit=False)
            newmaterial.classroom = ClassRoom(pk=classroom_pk)
            newmaterial.uploader = User(request.user.id)
            newmaterial.save()
            messages.success(request, 'File Upload Successful')
            return redirect('viewCreatedReadingMaterial', classroom_pk)
        else:
            return render(request, "create_join_class/uploadReadingMaterial.html", {'form': form})


@login_required
def deleteReadingMaterial(request, classroom_pk, readingMaterial_pk):
    if request.method == "POST":
        readingmaterial = ReadingMaterial.objects.get(pk=readingMaterial_pk)
        readingmaterial.delete()
        return redirect('viewCreatedReadingMaterial', classroom_pk)


@login_required
def viewCreatedReadingMaterial(request, created_pk):
    materialTeacher = ReadingMaterial.objects.filter(classroom_id=created_pk, uploader=request.user)
    return render(request, "create_join_class/viewCreatedReadingMaterial.html", {'materialTeacher': materialTeacher})


@login_required
def viewJoinedReadingMaterial(request, joined_pk):
    materialStudent = ReadingMaterial.objects.filter(classroom_id=joined_pk, classroom__students__in=[request.user.id])
    return render(request, "create_join_class/viewJoinedReadingMaterial.html", {'materialStudent': materialStudent})


def push_reading_info(request, readingMaterial_id):
    totalTimeSpentOnPage = request.POST.get('count')
    username = request.POST.get('username')
    print("Username: "+ username)
    print("TOTAL TIME SPENT: ", totalTimeSpentOnPage)
    reading_infos = {username: totalTimeSpentOnPage}
    reading_info = json.dumps(reading_infos)
    reading_info_obj = ReadingInfo.objects.create(material_id=ReadingMaterial.objects.get(id=readingMaterial_id),
                                                      material_info=reading_info)
    reading_info_obj.save()


@login_required
def view_reading_info(request, readingMaterial_id):
    try:
        reading_info_obj = ReadingInfo.objects.get(material_id=ReadingMaterial.objects.get(id=readingMaterial_id))
        reading_info_dict = json.loads(reading_info_obj.material_info)
        return render(request, "create_join_class/view_reading_info.html", {'reading_info_dict': reading_info_dict})
    except ReadingInfo.DoesNotExist:
        return render(request, "create_join_class/view_reading_info.html", {'reading_info_dict': 'This Material does '
                                                                                                 'not have any '
                                                                                                 'reading info in DB'})
    except ReadingMaterial.DoesNotExist:
        return render(request, "create_join_class/view_reading_info.html",
                      {'reading_info_dict': 'Reading Material Does Not Exists'})


@login_required
def uploadFaceImage(request):
    if request.method == 'GET':
        form = FaceImageForm()
        return render(request, "create_join_class/uploadFaceImage.html", {'form': form})
    else:
        form = FaceImageForm(request.POST, request.FILES)
        files = request.FILES.getlist('imageFile')
        if form.is_valid():
            for f in files:
                image = face_recognition.api.load_image_file(f)
                faces_in_a_image = face_recognition.api.face_locations(image)
                if faces_in_a_image:
                    file = FaceImage(imageFile=f)
                    file.name = User(request.user.id)
                    file.save()
                    messages.success(request, f'Face detected in Image. Upload Successful!')
                else:
                    messages.error(request, f'Face NOT detected in Image. Upload Failed!')
            return redirect('home_classroom')
        else:
            return render(request, "create_join_class/uploadFaceImage.html", {'form': form})


@login_required
def viewPDF(request, filename, material_id):
    return render(request, "create_join_class/viewPDF.html", {'filename': filename, 'material_id': material_id,
                                                              'username': request.user.username})


face_locations = []
face_encodings = []


@login_required
def facedetect(request):
    try:
        faceimages = FaceImage.objects.filter(name=request.user.id)
        url = ""
        for faceimage in faceimages:
            url = faceimage.imageFile.url
            url = "media" + url
            break
        # Get a reference to webcam #0 (the default one)
        video_capture = cv2.VideoCapture(0)

        # Load a sample picture and learn how to recognize it.
        my_image = face_recognition.load_image_file(url)
        my_face_encoding = face_recognition.face_encodings(my_image)[0]

        # Grab a single frame of video
        s, img = video_capture.read()
        if s:

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Find face and face encodings in the selected frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            # See if the face is a match for my face encoding
            check = face_recognition.compare_faces(my_face_encoding, face_encodings)

            if True in check:
                value = {'value': 1}
                video_capture.release()
                print(value)
                return JsonResponse(value)
            else:
                value = {'value': -1}
                video_capture.release()
                print(value)
                return JsonResponse(value)

    except FaceImage.DoesNotExist:
        return redirect("home_classroom", {'noimageerror': 'Please upload Image before viewing the file!'})
