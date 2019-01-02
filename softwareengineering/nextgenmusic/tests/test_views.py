from django.test import RequestFactory, SimpleTestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User, AnonymousUser
from nextgenmusic.views import viewsongs, index, joinus, profile, signup, loginuser
from mixer.backend.django import mixer
import pytest

@pytest.mark.django_db
class TestViews:
    #Test widoku index
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

    #Test widoku joinus
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

    #Test widoku signup
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

    #Test widoku viewsongs
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

    #Test widoku loginuser
    def test_loginuser_anonymoususer_not_post_method(self):
        c = Client()
        response = c.get(reverse('loginuser'))

        assert (response.status_code == 200)
        assert (response.context['message'] == 'Niepodano wszystkich danych!')

    def test_loginuser_anonymoususer_post_method_wrong_data(self):
        #User.objects.create(username='janusz', password='qwerty')
        c = Client()
        response = c.post(reverse('loginuser'), {'email': 'janusz@o2.pl',
                                                 'password': 'qwerty'})
        assert (response.context['message'] == 'Niepoprawne dane!')
        assert (response.status_code == 200)

    def test_loginuser_anonymoususer_post_method_good_data(self):
        User.objects.create_user(username='janusz', password='qwerty')
        c = Client()
        response = c.post(reverse('loginuser'), {'email': 'janusz@o2.pl',
                                                 'password': 'qwerty'})

        assert (response.status_code == 302)

    def test_loginuser_logeduser(self):
        request = RequestFactory().get(reverse('loginuser'))
        request.user = User.objects.create_user(username='kamil')

        response = loginuser(request)

        assert (response.status_code == 302)

    def test_loginuser_anonymoususer_postmethod_invalid_form_data(self):
        c = Client()
        response = c.post(reverse('loginuser'), {'email': 'emailbezmalpy',
                                                 'password': 'qwerty'})

        assert (response.context['message'] == 'Niepoprawne dane!')
        assert (response.status_code == 200)