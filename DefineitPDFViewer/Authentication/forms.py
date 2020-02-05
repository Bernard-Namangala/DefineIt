from django import forms
from django.contrib.auth.models import User
import re
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(label="Email or Username", max_length=255,
                               widget=forms.TextInput(attrs={'id': 'username', 'name': 'username'}))
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'id': 'password', 'name': 'password'}))

    def clean_username(self, *args, **kwargs):
        username = self.cleaned_data['username']
        username_regex = re.compile(r"^\w+$")
        if "@" not in username:
            if not username_regex.match(username):
                raise forms.ValidationError("Username contains invalid characters")
            else:
                if len(username) < 4:
                    raise forms.ValidationError("Username is too short")
                else:
                    if len(username) > 20:
                        raise forms.ValidationError("Username is too long")
                    else:
                        if not User.objects.filter(username=username):
                            raise forms.ValidationError("No user with such username exists")

        # if user wants to log in with email
        elif "@" in username:
            email_validator = EmailValidator()
            try:
                email_validator(username)
            except ValidationError:
                raise forms.ValidationError("invalid email!!")
            else:
                if not User.objects.filter(email=username):
                    raise forms.ValidationError("No user with such email exists")
        return username

    def clean_password(self, *args, **kwargs):
        password = self.cleaned_data['password']
        password_regex = re.compile(r"^[\w#@$?!]+$")
        if len(password) < 5:
            raise forms.ValidationError("Password is too short")
        else:
            if len(password) > 50:
                raise forms.ValidationError("Password is too long maximum of 50 characters is allowed")
            else:
                if not password_regex.match(password):
                    raise forms.ValidationError("Password contains invalid symbols allowed symbols are #@$?!*")
        return password


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'id': 'username', 'name': 'username'}))
    email_or_phone = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'id': 'email-phone',
                                                                                   'name': 'email_or_phone'}))
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'id': 'password', 'name': 'password'}))
    confirm_password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'id': 'con-password',
                                                                                         'name': 'con-password'}))

    def clean_username(self, *args, **kwargs):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)
        if user:
            raise forms.ValidationError("Username is already taken")
        else:
            username_regex = re.compile(r"^\w+$")
            if not username_regex.match(username):
                raise forms.ValidationError("Username contains invalid chracters")
            else:
                if len(username) < 4:
                    raise forms.ValidationError("Username is too short")
                else:
                    if len(username) > 20:
                        raise forms.ValidationError("Username is too long")
        return username

    def clean_email_or_phone(self, *args, **kwargs):
        email_or_phone = self.cleaned_data['email_or_phone']
        email_validator = EmailValidator()
        try:
            email_validator(email_or_phone)
        except ValidationError:
            raise forms.ValidationError("invalid email!!")
        user_with_email = User.objects.filter(email=email_or_phone)
        if user_with_email:
            raise forms.ValidationError("{}{}".format(email_or_phone, " is already associated with another account"))
        return email_or_phone

    def clean_password(self, *args, **kwargs):
        password = self.cleaned_data['password']
        password_regex = re.compile(r"^[\w#@$?!]+$")
        if len(password) < 5:
            raise forms.ValidationError("Password is too short")
        else:
            if len(password) > 50:
                raise forms.ValidationError("Password is too long maximum of 50 characters is allowed")
            else:
                if not password_regex.match(password):
                    raise forms.ValidationError("Password contains invalid symbols allowed symbols are #@$?!*")
        return password

    def clean_confirm_password(self, *args, **kwargs):
        confirm_password = self.cleaned_data['confirm_password']
        try:
            password = self.cleaned_data['password']
        except KeyError:
            password = ''
        if password:
            if not password == confirm_password:
                raise forms.ValidationError("Passwords do not match")
        return confirm_password
