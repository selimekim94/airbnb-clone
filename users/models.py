import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string


class User(AbstractUser):
    """ Custom User Model """
    GENDER_MALE = 'male'
    GENDER_FEMALE = 'female'
    GENDER_OTHER = 'other'

    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_OTHER, 'Other'),
    )

    LANGUAGE_EN = 'en'
    LANGUAGE_TR = 'tr'

    LANGUAGE_CHOICES = (
        (LANGUAGE_EN, 'English'),
        (LANGUAGE_TR, 'Turkish')
    )

    CURRENCY_USD = 'usd'
    CURRENCY_TRY = 'try'

    CURRENCY_CHOICES = (
        (CURRENCY_USD, 'USD'),
        (CURRENCY_TRY, 'TRY')
    )

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "Github"),
        (LOGIN_KAKAO, "Kakao"),
    )

    email = models.EmailField(_('email address'), unique=True)
    avatar = models.ImageField(upload_to='avatars', blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(blank=True, null=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=2, blank=True, default=LANGUAGE_TR)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3, blank=True, default=CURRENCY_TRY)
    super_host = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=20, default='', blank=True)
    login_method = models.CharField(
        max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            html_message = render_to_string(template_name='emails/verify_email.html', context={'secret': secret})
            send_mail(
                subject='Verify your account.',
                message=strip_tags(html_message),
                from_email='apikey',
                recipient_list=[self.email, ],
                fail_silently=False,
                html_message=html_message
            )
            self.save()
        return
