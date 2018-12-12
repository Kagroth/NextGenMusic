from django.shortcuts import render
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login
from pathlib import Path
from mutagen.mp3 import EasyMP3
from datetime import timedelta
from .utils import calculateSongDuration, getSongDataAsDict



def index(request):
    return render(request, 'nextgenmusic/index.html')

def viewsongs(request):
    songs = []
    id = 1
    musicFolder = Path('nextgenmusic/music')
    if request.GET.get('search') is None:
        for musicFile in musicFolder.iterdir():
            audiofile = EasyMP3(musicFile)
            duration = calculateSongDuration(audiofile)
            songs.append(getSongDataAsDict(audiofile, duration, id))
            id += 1
    else:
        toSearch = request.GET['search'].lower()
        for musicFile in musicFolder.iterdir():
            audiofile = EasyMP3(musicFile)

            if toSearch in audiofile['title'][0].lower():
                duration = calculateSongDuration(audiofile)
                songs.append(getSongDataAsDict(audiofile, duration, id))
                id += 1
                continue
            else:
                for artist in audiofile['artist']:
                    if toSearch in artist.lower():
                        duration = calculateSongDuration(audiofile)
                        songs.append(getSongDataAsDict(audiofile, duration, id))
                        id += 1
                        break

    return render(request, 'nextgenmusic/findmusic.html', {'songs': songs})

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


def loginuser(request):
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            user = authenticate(username=request.POST.get('email').split('@')[0], password=request.POST.get('password'))

            if user is not None:
                login(request, user)
                return HttpResponse("Zalogowano!")
            else:
                return HttpResponse("Bledne dane logowania!")
        else:
            return HttpResponse("Podano niepoprawne dane!")
    else:
        return HttpResponse("Nie podano wszystkich danych!")

