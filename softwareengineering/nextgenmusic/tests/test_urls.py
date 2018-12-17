from django.urls import reverse, resolve


class TestUrls:

    def test_viewsongs_url(self):
        path = reverse('viewsongs')
        assert resolve(path).view_name == 'viewsongs'

    def test_joinus_url(self):
        path = reverse('joinus')
        assert resolve(path).view_name == 'joinus'

    def test_signup_url(self):
        path = reverse('signup')
        assert resolve(path).view_name == 'signup'

    def test_loginuser_url(self):
        path = reverse('loginuser')
        assert resolve(path).view_name == 'loginuser'

    def test_profile_url(self):
        path = reverse('profile')
        assert resolve(path).view_name == 'profile'

    def test_logout_url(self):
        path = reverse('logout')
        assert resolve(path).view_name == 'logout'

