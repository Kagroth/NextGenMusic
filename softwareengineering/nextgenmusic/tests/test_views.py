from django.test import RequestFactory, SimpleTestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User, AnonymousUser
from nextgenmusic.views import viewsongs, index, joinus, profile, signup
from mixer.backend.django import mixer
import pytest

@pytest.mark.django_db
class TestViews:
    def test_index_anonymoususer(self):
        request = RequestFactory().get('/')
        request.user = AnonymousUser()

        response = index(request)
        assert (response.status_code == 200)
    
    def test_index_logeduser(self):
        request = RequestFactory().get('/')
        request.user = User.objects.create_user(username='kamil')

        response = index(request)
        assert (response.status_code == 200)

    def test_joinus_anonymoususer(self):
        request = RequestFactory().get('/joinus/')
        request.user = AnonymousUser()

        response = joinus(request)
        assert (response.status_code == 200)

    def test_joinus_logeduser(self):
        request = RequestFactory().get('/joinus/')
        request.user = User.objects.create_user(username='kamil')

        response = joinus(request)
        assert (response.status_code == 302)
    
    def test_signup_anonymoususer_no_data(self):    
        request = RequestFactory().get('/signup/')
        request.user = AnonymousUser()

        response = signup(request)
        assert (response.status_code == 200)

    def test_signup_anonymoususer_with_data(self):
        c = Client()
        response = c.post('/signup/', {'name': 'imie',
                            'surname': 'nazwisko',
                            'email': 'jakismail@server.com',
                            'password': 'haslo',
                            'repeat_password': 'haslo'})
        assert (response.context['message'] == "Rejestracja przebiegła pomyślnie!")

    def test_signup_logeduser(self):
        request = RequestFactory().get('/signup/')
        request.user = User.objects.create_user(username='kamil')

        response = signup(request)
        assert (response.status_code == 302)
        
    def test_viewsongs_authenticated(self):
        path = reverse('viewsongs')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)

        response = viewsongs(request)
        assert (response.status_code == 200)


    def test_viewsongs_unauthenticated(self):
        path = reverse('viewsongs')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()

        response = viewsongs(request)
        assert (response.status_code == 200)
