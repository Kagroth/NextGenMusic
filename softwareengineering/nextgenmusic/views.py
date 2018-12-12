from django.shortcuts import render
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.template import loader



def index(request):
    return render(request, 'nextgenmusic/index.html')

def viewsongs(request):
    return render(request, 'nextgenmusic/findmusic.html')

def joinus(request):
    return render(request, 'nextgenmusic/joinus.html')

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            #name = form.cleaned_data.get('name')
            User.objects.create_user(username=email.split("@")[0], email=request.POST.get('email'), password=request.POST.get('password'), first_name=request.POST.get('name'), last_name=request.POST.get('surname'))
            return render(request, 'nextgenmusic/index.html')
        else:
            return HttpResponse(request.POST.get('repeat_password'))
    return HttpResponse(request.POST.get('name'))
