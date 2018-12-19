
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from pathlib import Path
from mutagen.mp3 import EasyMP3
from datetime import timedelta
from .utils import calculateSongDuration, getSongDataAsDict
from .models import Playlist


def index(request):
    return render(request, 'nextgenmusic/index.html')

def viewsongs(request):
    songs = []
    id = 1
    musicFolder = Path('./nextgenmusic/static/nextgenmusic/music')
    if request.GET.get('search') is None:
        for musicFile in musicFolder.iterdir():
            duration = calculateSongDuration(musicFile)
            songs.append(getSongDataAsDict(musicFile, duration, id))
            id += 1
    else:
        toSearch = request.GET['search'].lower()
        for musicFile in musicFolder.iterdir():

            if toSearch in audiofile['title'][0].lower():
                duration = calculateSongDuration(musicFile)
                songs.append(getSongDataAsDict(musicFile, duration, id))
                id += 1
                continue
            else:
                for artist in audiofile['artist']:
                    if toSearch in artist.lower():
                        duration = calculateSongDuration(musicFile)
                        songs.append(getSongDataAsDict(musicFile, duration, id))
                        id += 1
                        break

    if request.user.is_authenticated:
        return render(request, 'nextgenmusic/logedfindmusic.html', {'songs': songs})

    return render(request, 'nextgenmusic/findmusic.html', {'songs': songs})

def joinus(request):
    if request.user.is_authenticated:
        return redirect('profile')

    return render(request, 'nextgenmusic/joinus.html')

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            #name = form.cleaned_data.get('name')
            try:
                User.objects.create_user(username=email.split("@")[0], email=request.POST.get('email'), password=request.POST.get('password'), first_name=request.POST.get('name'), last_name=request.POST.get('surname'))
            except:
                return render(request, 'nextgenmusic/welcome.html',
                              {'message': 'Niestety nie udało się zarejestrować',
                               'buttonText': 'Ponów',
                               'buttonHref': '../joinus/'})

            return render(request, 'nextgenmusic/welcome.html',
                          {'message': 'Rejestracja przebiegła pomyślnie!',
                           'buttonText': 'Zaloguj',
                           'buttonHref': '../joinus/'})

    return signup(request)


def loginuser(request):
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            user = authenticate(username=request.POST.get('email').split('@')[0], password=request.POST.get('password'))

            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                return render(request, 'nextgenmusic/welcome.html',
                              {'message': 'Niepoprawne dane!',
                               'buttonText': 'Ponów',
                               'buttonHref': '../joinus/'})
        else:
            return render(request, 'nextgenmusic/welcome.html',
                          {'message': 'Niepoprawne dane!',
                           'buttonText': 'Ponów',
                           'buttonHref': '../joinus/'})
    else:
        return render(request, 'nextgenmusic/welcome.html',
                      {'message': 'Niepodano wszystkich danych!',
                       'buttonText': 'Ponów',
                       'buttonHref': '../joinus/'})

def logoutuser(request):
    logout(request)
    return redirect('index')

def profile(request):
    if request.user.is_authenticated:
        try:
            playlists = Playlist.objects.filter(id_user=request.user)
        except:
            playlists = None
        return render(request, 'nextgenmusic/myprofile.html', {'user': request.user, 'playlists': playlists})
    else:
        return redirect('index')

def playlist(request, playlist_name):
    if request.user.is_authenticated:
        print("Bede pobieral playliste!")
        playlist = Playlist.objects.get(id_user=request.user, name=playlist_name)
        return render(request, 'nextgenmusic/playlist.html', {'user': request.user, 'playlist': playlist})
        try:
            print("Bede pobieral playliste!")
            playlist = Playlist.objects.get(id_user=request.user, name=playlist_name)
            return render(request, 'nextgenmusic/playlist.html', {'user': request.user, 'playlist': playlist})
        except:
            print("Nie znalazlem playlisty!")
            return redirect('profile')
    else:
        return redirect('index')
    
def createPlaylist(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.POST.get("playlistName") != "":
                playlistName = request.POST.get('playlistName')
                try:
                    exists = Playlist.objects.filter(id_user=request.user, name=playlistName).exists()
                except:
                    exists = False

                if exists:
                    print("Playlista o tej nazwie juz istnieje!")
                    return redirect('profile')
                else:
                    print("Tworze playliste!")
                    p = Playlist.objects.create(id_user=request.user, name=playlistName)
                    p.save()
                    return redirect('profile')
            else:
                print("Nie dostalem danych!")
                return redirect('profile')
        else:
            print("TO nie jest metoda POST!")
            return redirect('profile')
    else:
        print("User nie jest zalogowany!")
        return redirect('profile')

def deletePlaylist(request, playlist_name):
    print("Wchodze do widoku usuwania playlist!")
    if request.user.is_authenticated:
        print("Usuwam playliste!")
        playlist = Playlist.objects.filter(id_user=request.user, name=playlist_name).delete()
        return redirect('profile')

        
