from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('viewsongs/', views.viewsongs, name='viewsongs'),
    path('joinus/', views.joinus, name='joinus'),
    path('signup/', views.signup, name='signup'),
    path('login_user/', views.loginuser, name='loginuser')
]