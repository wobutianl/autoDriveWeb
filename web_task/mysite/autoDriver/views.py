from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def setCancelTask(request, pid):
    print(pid )
    return HttpResponse("Hello, world. ")
    pass