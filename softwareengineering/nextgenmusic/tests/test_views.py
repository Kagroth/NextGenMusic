from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from nextgenmusic.views import viewsongs
from mixer.backend.django import mixer
import pytest

@pytest.mark.django_db
class TestViews:

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
