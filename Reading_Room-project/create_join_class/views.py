from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate


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


def home_classroom(request):
    return render(request, 'create_join_class/home_classroom.html', {'user': request.user})
