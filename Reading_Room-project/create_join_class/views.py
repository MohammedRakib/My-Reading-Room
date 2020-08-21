from django.shortcuts import render


def index(request):
    return render(request, 'create_join_class/index.html')
