from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'email', 'password1', 'password2',)
        # fields = (
        #     'email', 'password1', 'password2', 'avatar', 'gender', 'bio', 'birth_date', 'language', 'currency',)

    def save(self, commit=True):
        """ Intercept and control saving a django form """
        user = super().save(commit=False)
        user.username = self.cleaned_data.get('email')
        user.save()
        user.verify_email()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = UserChangeForm.Meta.fields
