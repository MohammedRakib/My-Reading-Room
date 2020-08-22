import uuid
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import CreateClassRoomForm
from .models import ClassRoom


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
    return render(request, 'create_join_class/home_classroom.html',
                  {'user': request.user, 'classes': created_classes})
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
            # created_classes = ClassRoom.objects.filter(teacher=request.user)
            # return render(request, 'create_join_class/home_classroom.html',
            #               {'user': request.user, 'classes': created_classes})
            return redirect('home_classroom')
        except ValueError:
            return render(request, 'create_join_class/create_class.html',
                          {'form': CreateClassRoomForm, 'error': 'Bad data passed in. Try again!'})
