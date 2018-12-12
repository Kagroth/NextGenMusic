from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from pathlib import Path
from mutagen.mp3 import EasyMP3
from datetime import timedelta

# Create your views here.

def index(request):
    return render(request, 'nextgenmusic/index.html')

def viewsongs(request):
    songs = []
    id = 1
    musicFolder = Path('nextgenmusic/music')
    for musicFile in musicFolder.iterdir():
        audiofile = EasyMP3(musicFile)
        #okreslenie liczby minut
        minutes = int(audiofile.info.length // 60)
        #okreslenie liczby sekund oraz dodatnie do liczby minut
        seconds = round(minutes + audiofile.info.length % 60)
        duration = str(minutes) + ":" + str(seconds)
        songs.append(
            {'id': id,
             'artist': audiofile['artist'],
             'title': audiofile['title'][0], # tytul jest zawsze jeden, wiec biore pierwszy element
             'duration': duration})
        id += 1
    return render(request, 'nextgenmusic/findmusic.html', {'songs': songs})

def joinus(request):
    return render(request, 'nextgenmusic/joinus.html')