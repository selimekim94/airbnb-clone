from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, View
from .forms import CustomUserCreationForm
from .models import User


# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('core:home')
        return super().dispatch(*args, **kwargs)


class CustomLogoutView(LogoutView):
    pass


class CustomSignupView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('core:home')
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
            user.save()
        except User.DoesNotExist:
            pass
        return redirect(reverse('core:home'))
