from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader

# Create your views here.

def index(request):
    return render(request, 'nextgenmusic/index.html')

def viewsongs(request):
    return render(request, 'nextgenmusic/findmusic.html')

def joinus(request):
    return render(request, 'nextgenmusic/joinus.html')