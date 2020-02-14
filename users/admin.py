from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """ Custom User Admin """
    model = User
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    fieldsets = UserAdmin.fieldsets + (
        (
            'Custom Profile',
            {'fields': ('avatar', 'gender', 'bio', 'birth_date', 'language', 'currency', 'email_secret', 'super_host',
                        'email_verified',)}
        ),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    # add_fieldsets = UserAdmin.fieldsets + (
    #     (
    #         None,
    #         {
    #             "classes": ("wide",),
    #             "fields": ('avatar', 'gender', 'bio', 'birth_date', 'language', 'currency',)
    #         },
    #     ),
    # )

    list_filter = UserAdmin.list_filter + ('super_host',)

    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'is_active',
        'language',
        'currency',
        'email_secret',
        'super_host',
        'email_verified',
        'is_staff',
        'is_superuser',
    )
