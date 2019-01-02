
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth import authenticate, login, logout
from pathlib import Path
from mutagen.mp3 import EasyMP3
from datetime import timedelta
from .utils import calculateSongDuration, getSongDataAsDict
from .models import Playlist, Song
from django.core.files.storage import FileSystemStorage

import os

# widok strony glownej
def index(request):
    return render(request, 'nextgenmusic/index.html')

# widok wyswietlajacy liste utworow
def viewsongs(request):
    print("Pobieram piosenki!")
    songs = []
    id = 1
    currDir = os.path.dirname(__file__)
    projectDir = os.path.abspath(os.path.dirname(currDir))
    pathWithMusic = os.path.join(projectDir, 'nextgenmusic/static/nextgenmusic/music')
    print(pathWithMusic)
    musicFolder = Path(pathWithMusic)
    if request.GET.get('search') is None:
        for musicFile in musicFolder.iterdir():
            print(musicFile)
            duration = calculateSongDuration(musicFile)
            songs.append(getSongDataAsDict(musicFile, duration, id))
            id += 1
    else:
        print("wyszukuje piosenek!!")
        toSearch = request.GET['search'].lower()
        for musicFile in musicFolder.iterdir():
            audiofile = EasyMP3(musicFile)
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
        playlists = Playlist.objects.filter(id_user=request.user)
        return render(request, 'nextgenmusic/logedfindmusic.html', {'songs': songs, 'playlists': playlists})

    return render(request, 'nextgenmusic/findmusic.html', {'songs': songs})

# widok strony z logowaniem i rejestracja
def joinus(request):
    if request.user.is_authenticated:
        return redirect('profile')

    return render(request, 'nextgenmusic/joinus.html')

# widok odpowiedzialny za rejestracje
def signup(request):
    if request.user.is_authenticated:
        return redirect('profile')

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
        else:
            return render(request, 'nextgenmusic/welcome.html',
                          {'message': 'Nie podano wszystkich danych!',
                           'buttonText': 'Spróbuj ponownie',
                           'buttonHref': '../joinus/'})

    return joinus(request)


# widok odpowiedzialny za logowanie
def loginuser(request):
    if request.user.is_authenticated:
        return redirect('profile')
    
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

# widok odpowiedzialny za wylogowanie
def logoutuser(request):
    logout(request)
    return redirect('index')

# widok profilu uzytkownika
def profile(request):
    if request.user.is_authenticated:
        try:
            playlists = Playlist.objects.filter(id_user=request.user)
        except:
            playlists = None
        return render(request, 'nextgenmusic/myprofile.html', {'user': request.user, 'playlists': playlists})
    else:
        return redirect('index')

# wyświetla dane zawarte w playliscie - nazwe i liste piosenek
def playlist(request, playlist_name):
    if request.user.is_authenticated:
        print("Bede pobieral playliste!")
        try:
            print("Bede pobieral playliste!")
            playlist = Playlist.objects.get(id_user=request.user, name=playlist_name)
            print(playlist.songs)

            songsInPlaylist = []
            currDir = os.path.dirname(__file__)
            projectDir = os.path.abspath(os.path.dirname(currDir))
            pathWithMusic = os.path.join(projectDir, 'nextgenmusic/static/nextgenmusic/music')
            print(pathWithMusic)
            print("Bede iterowal po piosenkach!")
            print(playlist.songs)
            #musicFolder = Path(pathWithMusic)
            id = 1

            for song in playlist.songs.all():
                print("Iteruje po piosenkach!")
                musicFilePath = pathWithMusic + "/" + song.title + ".mp3"
                print(musicFilePath)
                musicFile = Path(musicFilePath)
                print(musicFile)
                duration = calculateSongDuration(musicFile)
                s = getSongDataAsDict(musicFile, duration, id)
                print(s)
                songsInPlaylist.append(s)
                print(songsInPlaylist)
                id += 1

            return render(request, 'nextgenmusic/playlist.html', {'user': request.user, 'playlist': playlist, 'songs': songsInPlaylist})
        except:
            print("Nie znalazlem playlisty!")
            return redirect('profile')
    else:
        return redirect('index')

# widok odpowiedzialny za tworzenie playlisty
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

# widok wyswietlajacy formularz zmiany nazwy playlisty
def editPlaylistName(request, playlist_name):
    if request.user.is_authenticated:
        pl = Playlist.objects.get(id_user=request.user, name=playlist_name)
        return render(request, 'nextgenmusic/editplaylist.html', {'playlist': pl})

    return redirect('profile')

# widok odpowiedzialny za zmiane nazwy playlisty
def changePlaylistName(request):
    if request.user.is_authenticated:
        if request.method == "POST" and \
            request.POST.get("newPlaylistName") is not None and \
            request.POST.get("oldPlaylistName") is not None:

            oldName = request.POST.get('oldPlaylistName')
            newName = request.POST.get('newPlaylistName')

            pl = Playlist.objects.get(id_user=request.user, name=oldName)
            pl.name = newName
            pl.save()

            return redirect('profile')
        else:
            return redirect('editPlaylistName', request.POST.get('oldPlaylistName'))

    return redirect('index')

# widok odpowiedzialny za usuniecie playlisty
def deletePlaylist(request, playlist_name):
    print("Wchodze do widoku usuwania playlist!")
    if request.user.is_authenticated:
        print("Usuwam playliste!")
        playlist = Playlist.objects.filter(id_user=request.user, name=playlist_name).delete()
        return redirect('profile')

# dodaje piosenke do playlisty
def addSongToPlaylist(request):
    if request.user.is_authenticated:
        if request.method == 'POST' \
                and request.POST.get("playlistName") is not None \
                and request.POST.get("songName") is not None:
            # obsluga dodania utworu do playlisty
            plName = request.POST.get("playlistName")
            songName = request.POST.get("songName")

            pl = Playlist.objects.get(id_user=request.user, name=plName)

            isInPlaylist = False

            for song in pl.songs.all():
                if song.title == songName:
                    print("Utwor jest juz w playliscie!")
                    isInPlaylist = True
                    break

            if isInPlaylist:
                print("Zwracam komunikat ze utwor jest")
                return JsonResponse({'message': 'Utwor juz jest w playliscie'})

            song = Song.objects.get(title=songName)
            pl.songs.add(song)

            print("Zwracam komunikat ze utwor udalo sie dodac")
            return JsonResponse({'message': 'Utwór dodany'})
        else:
            return JsonResponse({'message': 'Niepoprawne dane'})
    else:
        return redirect('viewsongs')

# usuwa utwor z playlisty
def removeFromPlaylist(request):
    message = "Nie udalo sie usunac piosenki"
    if request.user.is_authenticated:
        if request.method == 'POST' \
                and request.POST.get("playlistName") is not None \
                and request.POST.get("songName") is not None:

            plName = request.POST.get("playlistName")
            songName = request.POST.get("songName")

            try:
                playlist = Playlist.objects.get(id_user=request.user, name=plName)
                songToRemove = Song.objects.get(title=songName)
                playlist.songs.remove(songToRemove)
                message = "Utwor zostal usuniety z playlisty"
            except:
                print("Cos poszlo nie tak")
                message = "Nie udalo sie usunac piosenki"
        else:
            message = "Brak wszystkich danych!"
    else:
        message = "Anonimowy uzytkownik!"

    return JsonResponse({'message': message})

# Widok odpowiedzialny za dodanie utworu muzycznego do bazy
def paneladmin(request):
    if request.user.is_authenticated:
        if request.method == 'POST' and request.FILES['musicUpload']:
            try:
                musicUpload = request.FILES['musicUpload']
                fs = FileSystemStorage()
                fs.save(musicUpload.name, musicUpload)
                msg = "Utwór został dodany!"
                print(musicUpload.name)
                print(fs.base_location)

                piosenka = Song(title=(musicUpload.name).split('.')[0])
                piosenka.save()

                return render(request, 'nextgenmusic/paneladmin.html', {'msg': msg})
            except:
                msg = "Nie udało się!"
                return render(request, 'nextgenmusic/paneladmin.html', {'msg': msg})

        return render(request, 'nextgenmusic/paneladmin.html')
