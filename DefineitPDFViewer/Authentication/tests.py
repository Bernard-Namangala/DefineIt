from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from .forms import LoginForm
from django.forms import CharField


class TestLoginView(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'bernard',
            'password': 'ilovecoding1@'
        }
        User.objects.create_user(**self.credentials)

    def test_to_see_if_user_can_login(self):
        get_response = self.client.get(reverse('authentication:login'))
        self.assertIs(get_response.status_code, 200)
        post_response = self.client.post(reverse('authentication:login'), self.credentials, follow=True)
        self.assertTrue(post_response.context['user'].is_authenticated)


class TestLoginForm(TestCase):

    def test_username_field_with_invalid_characters(self):
        response = self.client.post(reverse('authentication:login'), {'username': 'bernard', 'password':
                                                                      '123456789'}, follow=True)
        self.assertFormError(response, 'login_form', 'username', ['No user with such username exists'])

    def test_username_field_with_short_username(self):
        response = self.client.post(reverse('authentication:login'), {'username': 'be', 'password':
                                                                      '123456789'}, follow=True)
        self.assertFormError(response, 'login_form', 'username', ['Username is too short'])

    def test_username_field_with_long_username(self):
        response = self.client.post(reverse('authentication:login'), {'username': 'Thisusernameisusedtotest'
                                                                                  'anditislongerthan20characters',
                                                                                  'password':
                                                                      '123456789'}, follow=True)
        self.assertFormError(response, 'login_form', 'username', ['Username is too long'])

    def test_username_field_with_correct_username_when_user_does_not_exist_in_database(self):
        response = self.client.post(reverse('authentication:login'), {'username': 'bernard', 'password':
                                                                      '123456789'}, follow=True)
        self.assertFormError(response, 'login_form', 'username', ['No user with such username exists'])

    def test_username_field_with_incorrect_email(self):
        response = self.client.post(reverse('authentication:login'), {'username': 'bernard@ma', 'password':
                                                                      '123456789'}, follow=True)
        self.assertFormError(response, 'login_form', 'username', ['invalid email!!'])

    def test_username_field_with_correct_email_when_user_does_not_exist_in_database(self):
        response = self.client.post(reverse('authentication:login'), {'username': 'bernard@gmail.com', 'password':
                                                                      '123456789'}, follow=True)
        self.assertFormError(response, 'login_form', 'username', ['No user with such email exists'])

    def test_password_with_short_password(self):
        response = self.client.post(reverse('authentication:login'), {'username': 'be', 'password':
                                                                      '12'}, follow=True)
        self.assertFormError(response, 'login_form', 'password', ['Password is too short'])

    def test_password_with_long_password(self):
        response = self.client.post(reverse('authentication:login'), {'username': 'be', 'password':
                                                                      '124'*50}, follow=True)
        self.assertFormError(response, 'login_form', 'password', ['Password is too long maximum of '
                                                                  '50 characters is allowed'])

    def test_password_with_invalid_characters(self):
        response = self.client.post(reverse('authentication:login'), {'username': 'be', 'password':
                                                                      '124!!!()HNub'}, follow=True)
        self.assertFormError(response, 'login_form', 'password', ['Password contains invalid symbols '
                                                                  'allowed symbols are #@$?!*'])
