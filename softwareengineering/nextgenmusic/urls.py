from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('viewsongs/', views.viewsongs, name='viewsongs'),
    path('joinus/', views.joinus, name='joinus'),
    path('signup/', views.signup, name='signup'),
    path('login_user/', views.loginuser, name='loginuser'),
    path('myprofile/', views.profile, name='profile'),
    path('logout/', views.logoutuser, name='logout'),
    path('myprofile/<str:playlist_name>/', views.playlist, name="playlist"),
    path('createPlaylist/', views.createPlaylist, name="createPlaylist"),
    path('editPlaylistName/<str:playlist_name>', views.editPlaylistName, name='editPlaylistName'),
    path('changePlaylistName/', views.changePlaylistName, name='changePlaylistName'),
    path('deletePlaylist/<str:playlist_name>', views.deletePlaylist, name="deletePlaylist"),
    path('addToPlaylist/', views.addSongToPlaylist, name='addSongToPlaylist'),
    path('removeFromPlaylist/', views.removeFromPlaylist, name='removeFromPlaylist'),
    path('paneladmin/', views.paneladmin, name='paneladmin'),
    path('listenCountUpdate/', views.listenCountUpdate, name='listenCountUpdate'),
    path('raport/', views.raport, name='raport'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

