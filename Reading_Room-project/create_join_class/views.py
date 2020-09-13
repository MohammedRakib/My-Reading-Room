import uuid
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import CreateClassRoomForm, ReadingMaterialForm
from .models import *
import json


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
    # return render(request, 'create_join_class/home_classroom.html', {'user': request.user})


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
            return render(request, 'create_join_class/join_class.html', {'error': 'No class found with that class code!'})

        if classobj.teacher == request.user:
            return render(request, 'create_join_class/join_class.html', {'error': 'You are the teacher of this class!'})
        else:
            user=request.user
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

@login_required()
def uploadReadingMaterial(request, classroom_pk):
    if request.method == 'GET':
        form = ReadingMaterialForm()
        return render(request, "create_join_class/uploadReadingMaterial.html", {'form':form})
    else:
        form = ReadingMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            newmaterial = form.save(commit=False)
            newmaterial.classroom = ClassRoom(pk=classroom_pk)
            newmaterial.uploader = User(request.user.id)
            newmaterial.save()
            return redirect('viewCreatedReadingMaterial',classroom_pk)


def viewCreatedReadingMaterial(request, created_pk):
    materialTeacher = ReadingMaterial.objects.filter(classroom_id=created_pk)
    return render(request, "create_join_class/viewCreatedReadingMaterial.html",{'materialTeacher': materialTeacher})


def viewJoinedReadingMaterial(request, joined_pk):
    materialStudent = ReadingMaterial.objects.filter(classroom_id=joined_pk)
    return render(request, "create_join_class/viewJoinedReadingMaterial.html",{'materialStudent': materialStudent})


# def push_reading_info(request, readingMaterial_id):
#     reading_info = {
#         'sanaulla': [10, 20, 30, 40, 50],
#         'sana1': [60, 70, 80, 90, 100,0,0,0],
#     }
#
#     reading_info = json.dumps(reading_info)
#     reading_info_obj=ReadingInfo.objects.create(material_id=ReadingMaterial.objects.get(id=readingMaterial_id), material_info=reading_info)
#     reading_info_obj.save()

def view_reading_info(request, readingMaterial_id):
    try:
        reading_info_obj=ReadingInfo.objects.get(material_id=ReadingMaterial.objects.get(id=readingMaterial_id))
        reading_info_dict = json.loads(reading_info_obj.material_info)
        return render(request, "create_join_class/view_reading_info.html", {'reading_info_dict': reading_info_dict})
    except ReadingInfo.DoesNotExist:
        return render(request, "create_join_class/view_reading_info.html", {'reading_info_dict': 'This Material does '
                                                                                                 'not have any '
                                                                                                 'reading info in DB'})
    except ReadingMaterial.DoesNotExist:
        return render(request, "create_join_class/view_reading_info.html",
                      {'reading_info_dict': 'Reading Material Does Not Exists'})
