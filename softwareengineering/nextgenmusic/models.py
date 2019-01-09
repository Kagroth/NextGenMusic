from django.db import models
import datetime
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    country = CountryField()


class Author(models.Model):
    name = models.CharField(max_length=100)
    country = CountryField(blank=True, blank_label='(select country)')

    def __str__(self):
        return self.name


YEAR_CHOICES = []
for r in range(1900, (datetime.datetime.now().year + 1)):
    YEAR_CHOICES.append((r, r))


class Song(models.Model):
    title = models.CharField(max_length=50)
    release_date = models.IntegerField(('year'), max_length=4, choices=YEAR_CHOICES,
                                        default=datetime.datetime.now().year)
    authors = models.ManyToManyField(Author)

    def __str__(self):
        return self.title

class Playlist(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    songs = models.ManyToManyField(Song)

class Listen_count(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_song = models.ForeignKey(Song, on_delete=models.CASCADE)
    count = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.id_user.username + " - " + self.id_song.title + " == " + str(self.count)

    def __str__(self):
        return self.id_user.username + " - " + self.id_song.title