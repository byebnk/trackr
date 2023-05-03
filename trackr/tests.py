from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase

from .models import TrackEntry
from .signals import user_logged_in_callback


class UserLoggedInCallback(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.factory = RequestFactory()

    def test_callback_successfully(self):
        user = self.user_model.objects.create(username='test-user', is_staff=True)
        request = self.factory.get('/')
        request.user = user

        user_logged_in_callback(self.__class__, request=request, user=user)
        self.assertTrue(TrackEntry.objects.filter(principal=user).exists())

    def test_callback_with_non_staff_user(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()

        db_user = self.user_model.objects.create(username='test-user', is_staff=False)
        user_logged_in_callback(self.__class__, request=request, user=db_user)
        self.assertFalse(TrackEntry.objects.filter(principal=db_user).exists())

    def test_callback_login_mfa(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()

        db_user = self.user_model.objects.create(username='test-user', is_staff=True)
        user_logged_in_callback(self.__class__, request=request, user=db_user)
        self.assertTrue(TrackEntry.objects.filter(principal=db_user).exists())
