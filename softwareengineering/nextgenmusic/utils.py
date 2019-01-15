from mutagen.mp3 import EasyMP3
from .models import Listen_count
from django.db.models import Sum
from pathlib import Path
import os

# funkcja zwraca długosc utworu w formacie MM:SS
def calculateSongDuration(musicfile):
    audiofile = EasyMP3(musicfile)
    # okreslenie liczby minut
    minutes = int(audiofile.info.length // 60)
    # okreslenie liczby sekund oraz dodatnie do liczby minut
    seconds = round(minutes + audiofile.info.length % 60)
    duration = str(minutes) + ":" + str(seconds)
    return duration

# funkcja zwraca dane utworu w postaci słownika
def getSongDataAsDict(musicfile, duration, id):
    print("Tworze plik EasyMP3")
    audiofile = EasyMP3(musicfile)
    print("Zwracam info o pliku!")
    return {'id': id,
     'filename': musicfile.name,
     'artist': audiofile['artist'],
     'title': audiofile['title'][0],  # tytul jest zawsze jeden, wiec biore pierwszy element
     'duration': duration}

# funkcja pobierajaca 5 najpopularniejszych utworow w serwisie
def getTopSongs():
    print(os)
    ranking = None
    try:
        message = "Przed rankingiem"
        ranking = Listen_count.objects.values('id_song__title').annotate(ilosc_odtworzen=Sum('count')).order_by('-ilosc_odtworzen')[:5]
        message = "Po rankingu"
        print(ranking)
        songs = []
        songsPaths = []
        id = 1
        message = "Przed sciezkami"
        currDir = os.path.dirname(__file__)
        projectDir = os.path.abspath(os.path.dirname(currDir))
        pathWithMusic = os.path.join(projectDir, 'nextgenmusic/static/nextgenmusic/music')
        message = "Po sciezkach przed petla"

        for dict in ranking:
            songsPaths.append(pathWithMusic + "/" + dict['id_song__title'] + ".mp3")

        message = "Po uzupelnieniu songsPaths"

        for songPath in songsPaths:
            print(songPath)
            musicFile = Path(songPath)
            print(musicFile)
            duration = calculateSongDuration(musicFile)
            s = getSongDataAsDict(musicFile, duration, id)
            s['listen_count'] = ranking[id - 1]['ilosc_odtworzen']
            print(s)
            songs.append(s)
            id += 1
    except Exception as e:
        songs = None
        print(message)
        print(e)

    print(songs)
    return songs
