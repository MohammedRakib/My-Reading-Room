import json
import uuid
import cv2
import face_recognition
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateClassRoomForm, ReadingMaterialForm, FaceImageForm
from .models import *


# This method is used for logging in. It redirects the user to homepage if credentials match.
# Else it prompts the user to reenter credentials.
def index(request):
    if request.method == 'GET':
        return render(request, 'create_join_class/index.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'create_join_class/index.html',
                          {'form': AuthenticationForm(), 'error': 'Username or password is incorrect'})
        else:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home_classroom')


# This method is for any user to create an account first before doing anything else.
# It redirects the user to homepage if account is created successfully. Else it prompts the
# user to reenter his credentials.
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


# This method logs out the user from the site and redirects him/her to the login page.
@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')


# This method is the homepage where the user can see his/her created and joined classes.
# It returns the homepage.
@login_required
def home_classroom(request):
    created_classes = ClassRoom.objects.filter(teacher=request.user)
    joined_classes = ClassRoom.objects.filter(students__in=[request.user.id])
    return render(request, 'create_join_class/home_classroom.html',
                  {'user': request.user, 'created_classes': created_classes, 'joined_classes': joined_classes})


# This method is used to create class. It creates a class with the POST data retrieved from the user via form
# and also generates a unique class code for other users to join.
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


# This method is used to join class. It checks if the user has uploaded an image of himself and only then
# allows the user to enter the classroom code. If the code matches the user successfully jons the class. Else,
# the system prompts the user to reenter code.
@login_required
def join_class(request):
    if request.method == "GET":
        numberOfImage = FaceImage.objects.filter(name=request.user).count()
        if numberOfImage >= 1:
            return render(request, 'create_join_class/join_class.html',
                          {'ImageFound': f'System found {numberOfImage} image(s) of you in the DB'})
        else:
            return render(request, 'create_join_class/join_class.html',
                          {'ImageNotFound': 'Please upload at least one image before joining a class'})
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


# This method is used to show the created classrooms by a user.
# It returns a html page with links to all created classrooms.
@login_required
def viewcreatedclassroom(request, classroom_pk):
    classroom = get_object_or_404(ClassRoom, teacher=request.user, pk=classroom_pk)
    return render(request, "create_join_class/viewcreatedclassroom.html", {'classroom': classroom})


# This method is used to show the joined classrooms by a user.
# It returns a html page with links to all joined classrooms.
@login_required
def viewjoinedclassroom(request, classroom_pk):
    classroom = get_object_or_404(ClassRoom, students__in=[request.user.id], pk=classroom_pk)
    return render(request, "create_join_class/viewjoinedclassroom.html", {'classroom': classroom})


# This method is used to upload reading material by the teacher of the class. The teacher
# can only upload pdf files as reading material. If upload is successful, the teacher
# is redirected to the created classroom html. Else the teacher is prompted to upload the file again.
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


# This method is used to delete any reading material uploaded by the teacher of the class. The teacher
# can only delete pdf files.
@login_required
def deleteReadingMaterial(request, classroom_pk, readingMaterial_pk):
    if request.method == "POST":
        readingmaterial = ReadingMaterial.objects.get(pk=readingMaterial_pk)
        readingmaterial.delete()
        return redirect('viewCreatedReadingMaterial', classroom_pk)


# This method is used to view the created reading materials by the teacher.
# It shows all the reading materials created by the teacher for a particular class.
@login_required
def viewCreatedReadingMaterial(request, created_pk):
    materialTeacher = ReadingMaterial.objects.filter(classroom_id=created_pk, uploader=request.user)
    return render(request, "create_join_class/viewCreatedReadingMaterial.html", {'materialTeacher': materialTeacher})


# This method is used to view the reading materials as a student.
# It shows all the reading materials uploaded by the teacher for a particular class.
@login_required
def viewJoinedReadingMaterial(request, joined_pk):
    materialStudent = ReadingMaterial.objects.filter(classroom_id=joined_pk, classroom__students__in=[request.user.id])
    return render(request, "create_join_class/viewJoinedReadingMaterial.html", {'materialStudent': materialStudent})


# This method is used to send the student name and time spent on a reading material back to the database.
# Atfirst with ajax post call, it receives reading info when a student closes the reading material tab and
# then converts it to json to push the data into the database
def push_reading_info(request, readingMaterial_id):
    username = request.POST.get('username')
    totalTimeSpentOnPage = request.POST.get('count')

    try:
        readingInfoObj = ReadingInfo.objects.get(material_id=ReadingMaterial.objects.get(id=readingMaterial_id))
        print("READING INFO OBJECT FETCHED")
        reading_info_dict = json.loads(readingInfoObj.material_info)
        print("MATERIAL INFO CONVERTED TO DICT")
        if username in reading_info_dict:
            previous_value = reading_info_dict[username]
            reading_info_dict[username] = int(totalTimeSpentOnPage) + int(previous_value)
            readingInfoObj.material_info = json.dumps(reading_info_dict)
            readingInfoObj.save()
        else:
            reading_info_dict[username] = totalTimeSpentOnPage
            readingInfoObj.material_info = json.dumps(reading_info_dict)
            readingInfoObj.save()
        print("Username: " + username)
        print("TOTAL TIME SPENT: from try-----", totalTimeSpentOnPage)

    except:
        print("Username: " + username)
        print("TOTAL TIME SPENT: ", totalTimeSpentOnPage)
        reading_infos = {
            username: totalTimeSpentOnPage
        }
        reading_info = json.dumps(reading_infos)
        reading_info_obj = ReadingInfo.objects.create(material_id=ReadingMaterial.objects.get(id=readingMaterial_id),
                                                      material_info=reading_info)
        reading_info_obj.save()


# This method is used to show the teacher the time spent by each student on a particular reading material
# It returns a list of all students with their corresponding reading time of a particular material.
@login_required
def view_reading_info(request, readingMaterial_id):
    try:
        reading_info_obj = ReadingInfo.objects.get(material_id=ReadingMaterial.objects.get(id=readingMaterial_id))
        reading_info_dict = json.loads(reading_info_obj.material_info)
        return render(request, "create_join_class/view_reading_info.html", {'reading_info_dict': reading_info_dict})
    except ReadingInfo.DoesNotExist:
        return render(request, "create_join_class/view_reading_info.html", {'NotFoundError': 'This Material does '
                                                                                             'not have any '
                                                                                             'reading info in DB'})
    except ReadingMaterial.DoesNotExist:
        return render(request, "create_join_class/view_reading_info.html",
                      {'NotFoundError': 'Reading Material Does Not Exists'})

# THis method is used to upload image. A user can upload any image in the format jpeg, jpg or png
# as long as the system can detect a face in the image. If the file format is right and the system detects
# a face, the upload is successful. Else the upload fails and prompts the user to upload again.
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

# This method is used to show pdf files to the students and returns and a html page where the pdf file is
# embedded.
@login_required
def viewPDF(request, filename, material_id):
    return render(request, "create_join_class/viewPDF.html", {'filename': filename, 'material_id': material_id,
                                                              'username': request.user.username})

# This method is used to detect and recognise face of the student while he/she is viewing the reading material.
# It returns 1 if face is recognised else it returns -1 if face is not recognised.
face_locations = []
face_encodings = []
@login_required
def facedetect(request):
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
    my_face_encodings = face_recognition.face_encodings(my_image)

    if len(my_face_encodings)>0:
        my_face_encoding = my_face_encodings[0]


        # Grab a single frame of video
        s, img = video_capture.read()
        video_capture.release()
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
                print(value)
                return JsonResponse(value)
            else:
                value = {'value': -1}
                print(value)
                return JsonResponse(value)

        else:
            value = {'value': 0}
            print(value)
            return JsonResponse(value)
