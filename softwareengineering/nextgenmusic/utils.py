from mutagen.mp3 import EasyMP3

def calculateSongDuration(musicfile):
    audiofile = EasyMP3(musicfile)
    # okreslenie liczby minut
    minutes = int(audiofile.info.length // 60)
    # okreslenie liczby sekund oraz dodatnie do liczby minut
    seconds = round(minutes + audiofile.info.length % 60)
    duration = str(minutes) + ":" + str(seconds)
    return duration

def getSongDataAsDict(musicfile, duration, id):
    audiofile = EasyMP3(musicfile)
    return {'id': id,
     'filename': musicfile.name,
     'artist': audiofile['artist'],
     'title': audiofile['title'][0],  # tytul jest zawsze jeden, wiec biore pierwszy element
     'duration': duration}

#def getPlaylist():
