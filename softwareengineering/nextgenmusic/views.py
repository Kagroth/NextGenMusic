from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from pathlib import Path
from mutagen.mp3 import EasyMP3
from datetime import timedelta
from .utils import calculateSongDuration, getSongDataAsDict

# Create your views here.

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
            songs.append(getSongDataAsDict(audiofile, id))
            id += 1
    else:
        toSearch = request.GET['search'].lower()
        for musicFile in musicFolder.iterdir():
            audiofile = EasyMP3(musicFile)

            if toSearch in audiofile['title'][0].lower():
                duration = calculateSongDuration(audiofile)
                songs.append(getSongDataAsDict(audiofile, id))
                id += 1
                continue
            else:
                for artist in audiofile['artist']:
                    if toSearch in artist.lower():
                        duration = calculateSongDuration(audiofile)
                        songs.append(getSongDataAsDict(audiofile, id))
                        id += 1
                        break

    return render(request, 'nextgenmusic/findmusic.html', {'songs': songs})

def joinus(request):
    return render(request, 'nextgenmusic/joinus.html')