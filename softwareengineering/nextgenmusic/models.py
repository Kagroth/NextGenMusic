from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	date_of_birth = models.DateField()
	country = CountryField()

class Author(models.Model):
	name = models.CharField(max_length=100)
	country = CountryField()
	
class Song(models.Model):
	title = models.CharField(max_length=50)
	release_date = models.DateField()
	
class Song_Author(models.Model):
	id_author = models.ForeignKey(Author, on_delete=models.CASCADE)
	id_song = models.ForeignKey(Song, on_delete=models.CASCADE)
	
class Playlist(models.Model):
	id_user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	
class Song_Playlist(models.Model):
	id_song = models.ForeignKey(Song, on_delete=models.CASCADE)
	id_playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
	
class Listen_count:
	id_user = models.ForeignKey(User, on_delete=models.CASCADE)
	id_song = models.ForeignKey(Song, on_delete=models.CASCADE)
	count = models.IntegerField()


	#pobieranie playlist użytkownika
	#pobieranie piosenek z playlisty