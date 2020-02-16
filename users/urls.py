from django.urls import path
from .views import (
    CustomLoginView,
    CustomLogoutView,
    CustomSignupView,
    CustomPasswordChangeView,
    CustomPasswordChangeDoneView,
    CompleteVerificationView,
    login_github,
    callback_github,
)

app_name = 'users'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('social/github/', login_github, name='login-github'),
    path('social/github/callback/', callback_github, name='callback-github'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', CustomSignupView.as_view(), name='signup'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change_done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('verify/<str:key>/', CompleteVerificationView.as_view(), name='complete-verification'),
]
