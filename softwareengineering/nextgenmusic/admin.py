from django.contrib import admin
from .models import Profile, Author, Song, Playlist, Listen_count

admin.site.register(Profile)
admin.site.register(Author)
admin.site.register(Song)
admin.site.register(Playlist)
admin.site.register(Listen_count)