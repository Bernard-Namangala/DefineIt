from django.shortcuts import render, redirect, reverse
from .forms import LoginForm, SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


def login_view(request):
    login_form = LoginForm(request.POST or None, label_suffix='')
    if login_form.is_valid():
        username = login_form.cleaned_data['username']
        password = login_form.cleaned_data['password']
        if "@" in username:
            user = User.objects.filter(email=username)
            if user:
                username = user[0].username
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        return redirect('/')

    context = {
        'login_form': login_form
    }

    return render(request=request, template_name='authentication/login.html', context=context)


def signup_view(request):
    sign_up_form = SignUpForm(request.POST or None, label_suffix='')

    if sign_up_form.is_valid():
        username = sign_up_form.cleaned_data['username']
        email_or_phone = sign_up_form.cleaned_data['email_or_phone']
        password = sign_up_form.cleaned_data['password']
        user = User.objects.create_user(username, email=email_or_phone, password=password)
        user.save()
        user = authenticate(username=username, password=password)
        login(request, user=user)
        return redirect('/')
    context = {
        'sign_up_form': sign_up_form,
    }
    return render(request=request, template_name='authentication/signup.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required()
def account_view(request, account_id):
    try:
        owner_of_account = User.objects.get(id=account_id)
    except User.DoesNotExist:
        return redirect(reverse('authentication:login'))
    else:
        context = {
            'user': owner_of_account
        }
        return render(request, template_name='authentication/account.html', context=context)
