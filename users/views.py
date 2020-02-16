import os
import requests
from django.contrib.auth import login
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, View
from django.core.files.base import ContentFile
from .forms import CustomUserCreationForm
from .models import User
from .exceptions import GithubException


# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('core:home'))
        return super().dispatch(*args, **kwargs)


class CustomLogoutView(LogoutView):
    pass


class CustomSignupView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('core:home'))
        return super().dispatch(*args, **kwargs)


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('users:password_change_done')


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'


class CompleteVerificationView(View):
    def get(self, *args, **kwargs):
        try:
            key = kwargs.get('key')
            user = User.objects.get(email_secret=key)
            user.email_verified = True
            user.email_secret = ''
            user.save()
        except User.DoesNotExist:
            pass
        return redirect(reverse('core:home'))


def login_github(request):
    client_id = os.environ.get('GITHUB_CLIENT_ID')
    redirect_uri = 'http://127.0.0.1:8000/users/social/github/callback'
    return redirect(
        f'https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user')


def callback_github(request):
    try:
        client_id = os.environ.get('GITHUB_CLIENT_ID')
        client_secret = os.environ.get('GITHUB_SECRET')
        code = request.GET.get('code', None)
        if code is not None:
            r = requests.post(url=
                              f'https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}',
                              headers={
                                  'Accept': 'application/json',
                              })
            data = r.json()
            error = data.get('error', None)
            if error is not None:
                raise GithubException()
            else:
                access_token = data.get('access_token')
                r = requests.get(url='https://api.github.com/user', headers={'Authorization': f'token {access_token}'})
                data = r.json()
                username = data.get('login', None)
                if username is not None:
                    name = data.get('name')
                    email = data.get('email', None)
                    bio = data.get('bio')
                    avatar_url = data.get('avatar_url', None)
                    if email is not None:
                        try:
                            user = User.objects.get(email=email)
                            if user.login_method != User.LOGIN_GITHUB:
                                raise GithubException()
                        except User.DoesNotExist:
                            user = User.objects.create(
                                email=email,
                                first_name=name,
                                username=email,
                                bio=bio,
                                login_method=User.LOGIN_GITHUB,
                                email_verified=True,
                            )
                            user.set_unusable_password()
                            user.save()
                            if avatar_url is not None:
                                r = requests.get(url=avatar_url)
                                user.avatar.save(f'{name}_avatar', ContentFile(r.content))
                        login(request, user)
                        return redirect(reverse('core:home'))
                    else:
                        raise GithubException('You don\'t have a public email on Github')
                else:
                    raise GithubException()
        else:
            raise GithubException()
    except GithubException:
        return redirect(reverse('users:login'))
